'''
Created on 12.07.2010

@author: ekondrashev
'''
import unittest
import logging

class BaseTestCase(unittest.TestCase):
    def assertEqual(self, value1, value2):
        #value1 = value1.decode('raw_unicode_escape')
        #value2 = value2.decode('raw_unicode_escape')
        if type(value1) is dict:
            if type(value2) is dict:
                self.assertEqualsDicts(value1, value2)
            else:
                raise self.failureException, 'value1 is dict, but value2 is not:  %s != %s' % (value1, value2)
        elif type(value1) is list:
            if type(value2) is list:
                unittest.TestCase.assertEqual(self, set(value1), set(value2), 'Not equals: %s != %s' %(set(value1), set(value2)) )
            else:
                raise self.failureException, 'value1 is list, but value2 is not:  %s != %s' % (value1, value2)
        else:
            unittest.TestCase.assertEqual(self, value1, value2, 'Not equals: %s != %s' %(value1, value2) )

    def assertEqualsLists(self, list1, list2):
        if len(list1) == len(list2):
            for itemL1 in list1:
                for itemL2 in list2:
                    if itemL1 == itemL2:
                        continue

    def assertEqualsDicts(self, dict1, dict2):
        unittest.TestCase.assertEqual(self, dict1, dict2, 'Not equals: %s != %s' % (self._dictToStr(dict1), self._dictToStr(dict2)) )

    def _dictToStr(self, dict):
        dictStr=u''
        for key, val in dict.items():
            dictStr += "'%s' : '%s'" % (key, val)
        return dictStr