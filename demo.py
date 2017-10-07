#!/usr/bin/env python

import requests
from base64 import b64encode
import json


district = "your.domain.net"
vsendpoint = ''.join(['voltage-pp-0000.', district])
protectURL = '/vibesimple/rest/v1/protect'
vs = ''.join(['https://', vsendpoint, protectURL])

plainSSNs = [ '012-34-5678', '123-45-6789' ]

authMethod = 'sharedSecret'
dataFormat = 'SSN'
identityPattern = ''.join(['PII@', district])
secret = 'MY_SOOPER_SEKRET_PASSWORD'
secret64 = b64encode(secret)

authHeader = 'VSAuth vsauth_method="{0}", vsauth_data="{1}", vsauth_identity_ascii="{2}", vsauth_version="{3}"'.format(authMethod, secret64, identityPattern, "200")

headers = { "content-type": "application/json", "Authorization": authHeader }

payload = { "format": dataFormat, "data": plainSSNs }


# r = requests.post(vs, headers=headers, data=json.dumps(payload)
# If you can't add the issuer's root certificate to cacert.pem, do not verify SSL/TLS:
r = requests.post(vs, headers=headers, data=json.dumps(payload), verify=False)

httpStatus = r.status_code
if httpStatus > 299:
    print('Error, HTTP status code {0}'.format(httpStatus))
    print(json.loads(r.text)['message'])
else:
    print('HTTP status code {0}'.format(httpStatus))
    print('Body: {0}'.format(r.text))

    responseData = json.loads(r.text)['data']

    if len(plainSSNs) == len(responseData):
        ssnCount = 0
        while ssnCount < len(plainSSNs):
            print('{0} =============> {1}'.format(plainSSNs[ssnCOunt], responseData[ssnCount]))
            ssnCount += 1


