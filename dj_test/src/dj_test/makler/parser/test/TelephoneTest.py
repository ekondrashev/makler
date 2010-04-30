'''
Created on 20.04.2010

@author: ekondrashev
'''
import unittest
from dj_test.makler import TELEPHONE_MATCHER

TELEPHONES = set([
u'0677401733',
u'050 552 34 74',
u'093-912- 04-41',
u'700 - 45 - 16',
u'0939120441',
u'7004516',
u'700 45 16'
])

class TelephoneMatcherTest(unittest.TestCase):

    def testTelephone(self):
        input = ','.join(TELEPHONES)
        (telephones, updated_input) = TELEPHONE_MATCHER.match(input)
        self.assertTrue(TELEPHONES, telephones)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()