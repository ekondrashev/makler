# -*- coding: utf-8 -*- 
'''
Created on 21.04.2010

@author: ekondrashev
'''
import unittest
from dj_test.makler import ROOM_COUNT_MATCHER, dispatchRoomCount

ROOM_COUNT = {
u'Сдам 4 к кв' : [4, u'Сдам '],
u'Старопортофранковская, Ольгиевская. 4 комн самост. кв. 3/3': [4,u'Старопортофранковская, Ольгиевская.  3/3'],
u'Сдам 1- к на Довженко' :[1, u'Сдам на Довженко'],
u'Сдам 2- х ком. квартиру, Большая Арнаутская/ Старопортофранковская, 4/ 5,': [2, u'Сдам , Большая Арнаутская/ Старопортофранковская, 4/ 5,'] ,
u'Сдам 1 ком. квартиру, ЖМ \\"Таирова\\",': [1, u'Сдам , ЖМ \\"Таирова\\",'],
u'Сдам 2- х ком. квартиру, Софиевская/ Торговая, 3/ 5':[2, u'Сдам , Софиевская/ Торговая, 3/ 5'],
}

class Test(unittest.TestCase):

    def testRoomCount(self):
        for input, result in ROOM_COUNT.iteritems():
            valid_room_count, valid_upd_input = result 
            (result_set, updated_input) = ROOM_COUNT_MATCHER.match(input)
            room_count = dispatchRoomCount(result_set)
            self.assertEqual(valid_room_count, room_count)
            self.assertEqual(valid_upd_input, updated_input)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()