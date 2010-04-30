import unittest

class BaseTestCase(unittest.TestCase):
	def assertEqual(self, value1, value2):
		#value1 = value1.decode('raw_unicode_escape')
		#value2 = value2.decode('raw_unicode_escape')
		unittest.TestCase.assertEqual(self, value1, value2, 'Not equals: %s != %s' %(value1, value2) )