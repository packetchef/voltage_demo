def testConfig():
	district = 'your.district.domain.com'
	testConfig = {
		'district': district,
		'sharedSecret': 'your_super_secret_password',
		'identityPattern': ''.join(['identity_pattern_1@', district])
	}
	return testConfig

