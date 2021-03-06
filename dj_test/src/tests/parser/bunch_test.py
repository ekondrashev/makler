'''
Created on 07.05.2010

@author: ekondrashev
'''

import os
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'

import unittest
import codecs
import json
import logging
from tests.parser.base_test_case import BaseTestCase
from dj_test.makler import findRoomCount, findCoast, findPhoneNumbers, findAddress

logging.basicConfig(level=logging.DEBUG)

TEST_ENTITIES = {
'roomCount' : findRoomCount,
'cost' : findCoast,
'phoneNumbers' : findPhoneNumbers,
'address' : findAddress,
}
INPUT = "input.json"
class Test(BaseTestCase):

	def testName(self):
		input = codecs.open(INPUT, "r", "utf-8" ).read()
		input1 = json.loads(input)
		for number, test in input1.iteritems():
			originalInput = test['originalInput']
			logging.info("Test #%s" % number)
			logging.info("Original advertisment text:\n%s" % originalInput)
			for testEntity, finder in TEST_ENTITIES.iteritems():
				originalValue = test[testEntity]
				foundValue = finder(originalInput)
				self.assertEqual(originalValue, foundValue)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()