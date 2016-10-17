import json
from hyper import HTTP20Connection
from hyper.tls import init_context
from apns2.conf import MAX_STREAM_NUM, CONNECTTION_STREAM_NUM


class Priority(object):
    Immediate = '10'
    Delayed = '5'


class APNsClient(object):
    def __init__(
            self, cert_file, use_sandbox=False,
            use_alternative_port=False, proto=None):
        if use_sandbox:
            self.server = 'api.development.push.apple.com'
        else:
            self.server = 'api.push.apple.com'
        self.port = 2197 if use_alternative_port else 443
        self.ssl_context = init_context()
        self.ssl_context.load_cert_chain(cert_file)
        self.proto = proto
        self.connection = HTTP20Connection(
            self.server, self.port, ssl_context=self.ssl_context,
            force_proto=self.proto or 'h2')
        self.response = {}

    def __create_headers(self, priority, topic=None, expiration=None):
        headers = {
            'apns-priority': priority
        }
        if topic:
            headers['apns-topic'] = topic

        if expiration is not None:
            headers['apns-expiration'] = "%d" % expiration
        return headers

    def __create_data(self, notification):
        json_payload = json.dumps(
            notification.dict(), ensure_ascii=False,
            separators=(',', ':')).encode('utf-8')
        return json_payload

    def __new_connection(self):
        self.connection = HTTP20Connection(
            self.server, self.port, ssl_context=self.ssl_context,
            force_proto=self.proto or 'h2')

    def __send_notification(self, token, json_payload, headers):
        url = '/3/device/{}'.format(token)
        try:
            stream_id = self.connection.request(
                'POST', url, json_payload, headers)
        except:
            self.__new_connection()
            stream_id = self.connection.request(
                'POST', url, json_payload, headers)
        return stream_id

    def send_notification_multiple(
            self, token_hexs, notification, topic=None, expiration=None,
            priority=Priority.Immediate):
        tokens_num = len(token_hexs)
        if tokens_num > MAX_STREAM_NUM:
            raise 'max tokens num is 3000'
        slice_num = tokens_num // CONNECTTION_STREAM_NUM
        if tokens_num % CONNECTTION_STREAM_NUM:
            slice_num += 1
        json_payload = self.__create_data(notification)
        headers = self.__create_headers(
            priority, topic=topic, expiration=expiration)
        for index in range(slice_num):
            stream_ids = {}
            for token in token_hexs[index * 500:(index + 1) * 500]:
                stream_id = self.__send_notification(
                    token, json_payload, headers)
                stream_ids[token] = stream_id
            self.get_response(self.connection, stream_ids)
        return self.response

    def get_response(self, connection, stream_ids):
        for token, stream_id in stream_ids.items():
            resp = connection.get_response(stream_id)
            if resp.status != 200:
                raw_data = resp.read().decode('utf-8')
                raw_data = json.loads(raw_data)
                self.response[token] = raw_data['reason']
