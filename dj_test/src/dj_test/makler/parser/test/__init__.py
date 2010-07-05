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
		else:
			unittest.TestCase.assertEqual(self, value1, value2, 'Not equals: %s != %s' %(value1, value2) )

	def assertEqualsDicts(self, dict1, dict2):
		unittest.TestCase.assertEqual(self, dict1, dict2, 'Not equals: %s != %s' % (self._dictToStr(dict1), self._dictToStr(dict2)) )

	def _dictToStr(self, dict):
		dictStr=u''
		for key, val in dict.items():
			dictStr += "'%s' : '%s'" % (key, val)
		return dictStr