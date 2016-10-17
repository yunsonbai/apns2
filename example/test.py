from apns2.client import APNsClient
from apns2.payload import Payload
import time


def push():
    # test
    token = '9dsfeg2fa913b390fc6b3d3ec637a764867241f516d847b54d24ce7e37963b6e'
    token_hexs = []
    for i in range(10):
        token_hexs.append(token)
    token_hexs.append('sss')
    payload = Payload(alert="Hello World!", sound="default")
    client = APNsClient(
        'Dev_Push_Cer-key.pem',
        # 'Release_Push_Cer_Key.pem',
        use_sandbox=True,
        use_alternative_port=False)

    st = time.time()
    response = client.send_notification_multiple(token_hexs, payload)
    et = time.time()
    print(et - st)
    print(response)

if __name__ == '__main__':
    push()
