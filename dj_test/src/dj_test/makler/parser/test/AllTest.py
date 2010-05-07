'''
Created on 07.05.2010

@author: ekondrashev
'''
import unittest
import codecs
import json
import logging
from dj_test.makler.parser.test import BaseTestCase
from dj_test.makler import findRoomCount

logging.basicConfig(level=logging.DEBUG)

TEST_ENTITIES = {
'roomCount' : findRoomCount,
#'coast',
#'address',
#'phoneNumbers',
}
INPUT = "input.json"
class Test(BaseTestCase):

	def testName(self):
		input = codecs.open(INPUT, "r", "utf-8" ).read()
		print input
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