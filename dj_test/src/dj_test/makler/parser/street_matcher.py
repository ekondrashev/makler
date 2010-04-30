# -*- coding: utf-8 -*- 
'''
Created on 28.04.2010

@author: ekondrashev
'''
import os, sys
import logging
import aspects
from dj_test.makler.parser.test import BaseTestCase
from dj_test.makler.utils import OrderedSet

logging.basicConfig(level=logging.DEBUG)
import unittest
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'

from dj_test.makler.parser.matcher import BaseMatcher, baseMatcher_cut_log,\
	baseMatcher_match_log
from dj_test.makler.models import Street, StreetFreak



class StreetMatcher(BaseMatcher):

	def __init__(self, patterns_str, lookingEntityName, replaceMatches = False, replacementString = '', matchLimit = 2):
		BaseMatcher.__init__(self, patterns_str, lookingEntityName, replaceMatches, replacementString)
		self.foundEntities = OrderedSet()
		self.limit = matchLimit

	def cut(self, match):
		for i in range(0,len(match.groups())):
			street_name = self.findStreet(match.group(i+1))
			if street_name:  
				self.foundEntities.append(street_name)
				#if (len(self.foundEntities) == self.limit):
				#	break
		return self.replacementString

	def _matchWithoutCut(self, input, pattern):
		for pretenders in pattern.findall(input):
			if pattern.groups == 1:
				pretenders = [pretenders]
			for pretender in pretenders:
				street_name = self.findStreet(pretender)
				if street_name:  
					self.foundEntities.add(street_name)
		return input

	def findStreet(self, name):
		streets = Street.objects.filter(name__contains=name)
		if streets:
			return streets[0].name
		else:
			street_freaks = StreetFreak.objects.filter(name__contains=name)
			if street_freaks:
				return street_freaks[0].street.name
		
	def match(self, input):
		self.foundEntities = OrderedSet()
		if self.replaceMatches:
			in_match = self._matchWithCut
		else:
			in_match = self._matchWithoutCut

		for pattern in self.patterns:
			input = in_match(input, pattern)
			if (len(self.foundEntities) >= self.limit):
				break
		return (self.foundEntities, input)

def streetMatcher__matchWithoutCut(*args, **kwargs):
	baseMatcher = args[0]
	input = args[1]
	pattern = args[2]
	logging.debug('%s:applying pattern: %s' % (baseMatcher.lookingEntityName, pattern.pattern))
	#logging.debug('Found pretender to %s: %s' % (baseMatcher.lookingEntityName, collection_str(match.groups())))
	retval = yield aspects.proceed(*args, **kwargs)
	yield aspects.return_stop(retval)

def streetMatcher_find_street(*args, **kwargs):
	name = args[1]
	retval = yield aspects.proceed(*args, **kwargs)
	if retval:
		logging.debug('									Accepted:      %s -> %s' % (name, retval))
	else:
		logging.debug('									Not accepted.. %s' % name)
	yield aspects.return_stop(retval)

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

aspects.with_wrap(baseMatcher_match_log, StreetMatcher.match)
aspects.with_wrap(baseMatcher_cut_log, StreetMatcher.cut)
aspects.with_wrap(streetMatcher_find_street, StreetMatcher.findStreet)
aspects.with_wrap(streetMatcher__matchWithoutCut, StreetMatcher._matchWithoutCut)
if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testFlatSquare']

	unittest.main()

	