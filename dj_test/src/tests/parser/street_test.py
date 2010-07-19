# -*- coding: utf-8 -*- 
'''
Created on 12.07.2010

@author: ekondrashev
'''
import os
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'

import unittest
from tests.parser.base_test_case import BaseTestCase
from dj_test.makler.parser.street_matcher import StreetMatcher

STREETS = {
u'Сдам 1 ком. кв. Тополева / Королева. 3/10эт. 57м – общая. Евроремонт. 2 лоджии застеклены. Гардеробная. Стеклопакеты. Импортная мебель, встроенная кухня. Вся бытовая техника. Тамбур. На длительный срок. 500у. е.' : ['Тополевая (Киевский)', 'Академика Королева'],
u'Бунина/ Канатная, 3/3. 2конт. АГВ, н.сант., МП окна во двор, с\у совмещен, облицован, необх. мебель, каб. ТВ, холод., стир. маш. авт. Чистая, уютная. СВОЯ БЕЗ ПОСРЕДНИКОВ!' : ['Бунина', 'Канатная'],
u'Старопортофранковская, Ольгиевская. 4 комн самост. кв. 3/3, 100м. Т/в раздельно. Агв. Балкон. Жилое. На длительно. От хозяина 600уе' : ['Старопортофранковская', 'Ольгиевская'],
u'Сдам 2х Неженская, Евроремонт, 300у. е.' : ['Нежинская', ''],
u'Сдам 2- х ком. квартиру, Большая Арнаутская/ Старопортофранковская, 4/ 5, "сталинка", комнаты раздельные, балкон застеклен, санузел облицован (т+ в), бытовая техника, стиральная машина- автомат, мебель МПО, бронир. дверь, парадная на коде, место для авто, цена: 3400 грн. (420 у. е.)': ['Большая Арнаутская', 'Старопортофранковская'],
u'Сдам 1 ком. квартиру, Ал. Невского ЖМ \\"Таирова\\", 5/ 10, новый дом, ремонт, мебель, бытовая техника, балкон, кабельное ТВ, интернет, МПО, бронир. дверь, цена: 2400 грн (300 у. е.)' : [u'Александра Невского', ''],
u'Сдам 2- х ком. квартиру, Александровский пр- т/Троицкая, 2/ 3, свежий ремонт, новая мебель, бытовая техника, стиральная машина- автомат, санузел облицован (т+ в), АГВ, колонка, кабельное ТВ, интернет, МПО, бронир. дверь, цена: 3000 грн. (380 у. е.)' : ['Александровский проспект', 'Троицкая'],
u'сдам 2 ком. кв. Итальянский бульвар / Канатная. 4/ 4эт. Сталинка. Комнаты раздельные – 20м +20м. Классический капремонт. Стеклопакеты. Импортная мебель, встроенная кухня. Вся бытовая техника. Кондиционер. Балкон застеклен. 7958312' : ['Итальянский бульвар', 'Канатная'],

}

#4 цена -> пер ГерЦЕНА
#5 новая -> ЗерНОВАЯ
STREET_MIN_CHAR_COUNT = 6
class Test(BaseTestCase):
    def testStreetMatcher(self):
        patterns = [
                    ur'(?u)([а-яА-Я]{%d,})\s*[а-яА-Я]*\s*/\s*([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT, STREET_MIN_CHAR_COUNT), # Not sure about this
                    ur'(?u)([а-яА-Я]{%d,})\s*\s*/\s*([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT, STREET_MIN_CHAR_COUNT),
                    ur'(?u)([а-яА-Я]{%d,})\s*,\s*([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT, STREET_MIN_CHAR_COUNT),
                    ur'(?u)([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT),
                    ]
        matcher = StreetMatcher(patterns, 'street')
        #print street_name, corner_street_name
        #print Street.objects.all()
        for input, valid_result in STREETS.iteritems():
            valid_street, valid_corner_street = valid_result
            result, updated_input = matcher.match(input)
            street = ''
            corner_street = ''
            if len(result) == 2:
                street = result.pop(False)
                corner_street = result.pop(False)
            else:
                street = result.pop()
            self.assertEqual(valid_street, street)
            self.assertEqual(valid_corner_street, corner_street)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFlatSquare']

    unittest.main()

