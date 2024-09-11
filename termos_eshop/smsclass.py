import requests
from django.conf import settings
apiKey = settings.SMS_API_TOKEN


# myclass (mehdi.kr@gmail.com 1401/04/25)
def send_otp_sms(verify_code, receiver_num):
    template = "TermosOTP"
    sms = Ghasedak(apiKey)
    sms.verification({'receptor': receiver_num, 'type': '1', 'template': template, 'param1': str(verify_code)})


def send_success_sms(user_full_name, order_id, receiver_num):
    template = "SuccessOrder"
    sms = Ghasedak(apiKey)
    sms.verification({'receptor': receiver_num, 'type': '1', 'template': template, 'param1': str(user_full_name), 'param2': str(order_id)})


def send_products_update_sms(product_ids, receiver_num):
    template = "ProductUpdate"
    sms = Ghasedak(apiKey)
    sms.verification({'receptor': receiver_num, 'type': '1', 'template': template, 'param1': str(product_ids)})


def send_sms_to_09187232987(message):
    sms = Ghasedak(apiKey)
    sms.send({'message': message, 'receptor': '09187232987', 'linenumber': '10008566'})
    sms.send({'message': message, 'receptor': '09187232987', 'linenumber': '100005858'})


def bulk(opts):
    data = {'path': "sms/send/pair?agent=python", 'data': {
        'message': opts['message'],
        'receptor': opts['receptor'],
        'linenumber': opts['linenumber'] if 'linenumber' in opts.keys() else "",
        'senddate': opts['senddate'] if 'senddate' in opts.keys() else "",
        'checkid': opts['checkid'] if 'checkid' in opts.keys() else ""
    }}
    return data


class Ghasedak:
    """docstring for Ghasedak."""

    def __init__(self, apikey):
        self.apikey = apikey

    # send request to api
    def request_api(self, opts):
        headers = {
            'Accept': "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            'charset': "utf-8",
            'apikey': self.apikey,

        }

        url = 'https://api.ghasedak.me/v2/' + opts['path']

        data = opts['data']

        r = requests.post(url, data=data, headers=headers)

        return r

    def status(self, opts):
        data = {'path': "sms/status?agent=python", 'data': {
            'id': opts['id'],
            'type': opts['type']
        }}

        r = self.request_api(data)

        jr = r.json()
        # print(jr["items"])

        if r.status_code == 200:
            return jr["items"]

        return []

    def send(self, opts):
        data = {'path': "sms/send/simple?agent=python", 'data': {
            'message': opts['message'],
            'receptor': opts['receptor'],
            'linenumber': opts['linenumber'] if 'linenumber' in opts.keys() else "",
            'senddate': opts['senddate'] if 'senddate' in opts.keys() else "",
            'checkid': opts['checkid'] if 'checkid' in opts.keys() else ""
        }}

        r = self.request_api(data)

        # # Get status data right after sending
        # jdata = json.loads(r.text)
        # self.status({str(jdata['items'][0]), '1'})

        if r.status_code == 200:
            return True

        return False

    def bulk1(self, opts):
        data = bulk(opts)

        r = self.request_api(data)
        if r.status_code == 200:
            return True

        return False

    def bulk2(self, opts):
        data = bulk(opts)

        r = self.request_api(data)
        if r.status_code == 200:
            return True

        return False

    def pair(self, opts):
        data = bulk(opts)

        r = self.request_api(data)
        if r.status_code == 200:
            return True

        return False

    def voicecall(self, opts):
        data = {'path': "voice/send?agent=python", 'data': {
            'message': opts['message'],
            'receptor': opts['receptor'],
            'senddate': opts['senddate'] if 'senddate' in opts.keys() else ""
        }}

        r = self.request_api(data)
        if r.status_code == 200:
            return True

        return False

    def verification(self, opts):
        data = {'path': "verification/send/simple?agent=python", 'data': {
            'receptor': '0' + str(int(opts['receptor'])),
            'type': opts['type'] if 'type' in opts.keys() else "",
            'template': opts['template'],
            'ip': opts['ip'] if 'ip' in opts.keys() else "",
            'param1': opts['param1'],
            'param2': opts['param2'] if 'param2' in opts.keys() else "",
            'param3': opts['param3'] if 'param3' in opts.keys() else ""
        }}

        r = self.request_api(data)
        if r.status_code == 200:
            return True

        return False

    def check_verification(self, opts):
        data = {'path': "sms/check/verification?agent=python", 'data': {
            'receptor': opts['receptor'],
            'token': opts['token'],
            'ip': opts['ip'] if 'ip' in opts.keys() else ""
        }}

        r = self.request_api(data)
        if r.status_code == 200:
            return True

        return False
