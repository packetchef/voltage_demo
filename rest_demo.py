#!/usr/bin/env python

import requests
import base64
import json
import sys
from demo_config import testConfig


def postAction(url, headers, payload, cafile):
	# If you can't add the issuer's root certificate to your cacert file or copied to
	# voltage_root.pem then use verify=False to not verify SSL/TLS
	try:
		r = requests.post(url, headers=headers, data=json.dumps(payload), verify=cafile)
	except IOError:
		r = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
	return r


def usage(args):
	pass


def main(args):

	config = testConfig()

	cafile = '.\\voltage_root.pem'
	district = config['district']
	vsendpoint = ''.join(['voltage-pp-0000.', district])
	protectURLbase = '/vibesimple/rest/v1/'

	authMethod = 'sharedSecret'
	dataFormat = args[1]
	identityPattern = config['identityPattern']
	secret = config['sharedSecret']
	secret64 = base64.b64encode(secret)

	authHeader = 'VSAuth vsauth_method="{0}", vsauth_data="{1}", vsauth_identity_ascii="{2}", vsauth_version="{3}"'.format(authMethod, secret64, identityPattern, "200")
	headers = {"content-type": "application/json", "Authorization": authHeader }

	action = args[0]
	if action == 'access':
		protectURL = 'access'
	elif action == 'protect':
		protectURL = 'protect'
	else:
		print('Invalid action type: {0}'.format(action))
		exit(1)

	vsURL = ''.join(['https://', vsendpoint, protectURLbase, action])

	inputVals = []
	for val in args[2:]:
		inputVals.append(val)

	# You can submit a single input value  or a bundle of values to be accesed or protected
	payload = { "format": dataFormat, "data": inputVals }

	response = postAction(vsURL, headers, payload, cafile)

	print('********************************************')
	httpStatus = response.status_code
	if httpStatus > 299:
		print('Error, HTTP status code {0}'.format(httpStatus))
		httpError = json.loads(response.text)['message']
		print('Error: {0}'.format(httpError))
		exit(1)
	else:
		print('HTTP status code {0}'.format(httpStatus))
		print('Body: {0}'.format(response.text))
		print('********************************************')


	responseData = json.loads(response.text)['data']
	if len(inputVals) == len(responseData):
		match = 0
		while match < len(inputVals):
			print('{0} ===================> {1}'.format(inputVals[match], responseData[match]))
			match += 1
		print('********************************************')
	else:
		print('Mismatch between number of input values ({0}) and number of returned values ({1})'.format(len(inputValues), len(responseData)))


if __name__ == '__main__':
	# Usage:
	# python rest_demo.py protect SSN 012-34-5678
	# python rest_demo.py protect SSN 012-34-5678 111223333
	# python rest_demo.py access SSN 497-22-3333
	main(sys.argv[1:])


