import os
import json
import requests

url = 'http://api.sendcloud.net/apiv2/mail/sendtemplate'


def sendtemplate(to, name, code_url):
    xsmtpapi = {
        'to': [to],
        'sub': {
            '%name%': [name],
            '%url%': [code_url],
        }
    }

    params = {
        'apiUser': os.environ['SEND_CLOUD_API_USER'],
        'apiKey': os.environ['SEND_CLOUD_API_KEY'],
        'templateInvokeName': 'express_register',
        'xsmtpapi': json.dumps(xsmtpapi),
        'from': os.environ['SEND_CLOUD_FROM'],
        'fromName': '同村传递',
        # 'subject': '同村传递 - 注册',
        'replyTo': os.environ['SEND_CLOUD_REPLY_TO'],
        'useNotification': 'true'
        # 是否使用回执
    }

    # filename = './test.txt'
    # display_filename = 'filename'

    # files = { 'attachments' : (urllib.quote(display_filename), open(filename,'rb'))}

    # r = requests.post(url, files=files, data=params)
    r = requests.post(url, data=params)

    print(r.text)
