# -*- coding: utf-8 -*- 
'''
Created on 22.04.2010

@author: ekondrashev
'''
import unittest
from dj_test.makler import COAST_MATCHER, dispatchCoast

COAST = {
u'Евроремонт, АГВ, 36м. кв. Хорошая транспортная развязка. Рядом Таврия. 300 у. е.' : [300, u'уе', u''],
u'Старопортофранковская, Ольгиевская. Агв. Балкон. Жилое. На длительно. От хозяина 600уе' : [600, u'уе', ''],
u'Довженко/ Шевченко, 1/ 5, \"сталинка\", квартира после капремонта, 3000 грн/ месяц. т. 7034410' : [3000, u'грн', u'месяц'],
u'интернет, МПО, бронир. дверь, цена: 450 у. е.' : [450, u'уе', u'']
}

class Test(unittest.TestCase):


    def testCoast(self):
        for input, result in COAST.iteritems():
            valid_room_count, valid_currency, valid_duration = result 
            (result_set, updated_input) = COAST_MATCHER.match(input)
            coast, currency , duration= dispatchCoast(result_set)
            self.assertEqual(valid_room_count, coast)
            self.assertEqual(valid_currency, currency)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCoast']
    unittest.main()