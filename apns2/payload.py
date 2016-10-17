from apns2.conf import MAX_PAYLOAD_SIZE


class PayloadAlert(object):
    def __init__(
            self, title=None, title_localized_key=None,
            title_localized_args=None, body=None, body_localized_key=None,
            body_localized_args=None, action_localized_key=None,
            launch_image=None):
        self.kwargs = {
            'title': title,
            'title-loc-key': title_localized_key,
            'title-loc-args': title_localized_args,
            'body': body,
            'loc-key': body_localized_key,
            'loc-args': body_localized_args,
            'action-loc-key': action_localized_key,
            'launch-image': launch_image
        }

    def dict(self):
        result = {}
        for key, value in self.kwargs.items():
            if value:
                result[key] = value
        return result


class Payload(object):
    def __init__(
            self, alert=None, badge=None, sound=None, content_available=False,
            mutable_content=False, category=None, custom=None):
        '''
        content_available: 0/1
        mutable_content: 0/1
        '''
        self.custom = custom
        if isinstance(alert, PayloadAlert):
            alert = alert.dict()
        self.kwargs = {
            'alert': alert,
            'badge': badge,
            'sound': sound,
            'content-available': 1 if content_available else 0,
            'mutable-content': 1 if mutable_content else 0,
            'category': category,
        }

    def dict(self):
        result = {
            'aps': {}
        }
        for key, value in self.kwargs.items():
            result['aps'][key] = value
        if self.custom:
            result.update(self.custom)
        return result
