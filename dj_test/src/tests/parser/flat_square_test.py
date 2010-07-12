# -*- coding: utf-8 -*- 
'''
Created on 22.04.2010

@author: ekondrashev
'''
import unittest
from dj_test.makler import FLAT_SQUARE_MATCHER, dispatchSquare

FLAT_SQUARE = {
u'36 м. кв., бель/ 2, Евроремонт,' : 36,
u' 4 комн самост. кв. 3/3, 100м. ' : 100,
}

class Test(unittest.TestCase):


    def testFlatSquare(self):
        for input, valid_square in FLAT_SQUARE.iteritems():
            (result_set, updated_input) = FLAT_SQUARE_MATCHER.match(input)
            square = dispatchSquare(result_set)
            self.assertEqual(valid_square, square)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFlatSquare']
    unittest.main()