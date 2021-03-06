# -*- coding: utf-8 -*- 

from dj_test.makler.parser.matcher import BaseMatcher
from dj_test.makler.parser.street_matcher import StreetMatcher

TELEPHONE_PATTERNS = [ 
ur'(?u)(8?0\d{2}\s?\-?\.?\s?\d{3}\s?\-?\s?\d{2}\s?\-?\s?\d{2})' ,#0677401733, 050 552 34 74, 22, 093-912-04-41, 096.487-72-05
ur'(?u)(\d{3}\s?\-?\s?\d{2}\s?\-?\s?\d{2})',  #700 45 16, 700 - 45 - 16
ur'(?u)(\d{7})', #7004516
]

#Возвращаемый результат один 
ROOM_COUNT_PATTERNS = [
ur'(?u)(\d+)\s*-?\s*х',					   
ur'(?u)(\d+)\s*-?\s*х?\s*ком\.?\s*квартиру',	 #2- х ком. квартиру, 1 ком квартиру
ur'(?u)(\d+)\s*комн\.?\s*(?:\w+\.?)?\s*кв\.?',   #4 комн самост. кв. #самост???
ur'(?u)(\d+)\s*-?\s*к\.?\s*к?в?\.?',			 #1- к, 4 к кв
#u'(\d+) ком\.? кв\.?',
#u'(\d+)\s*-\s*к\.?',	#1-к
#u'(\d+) комн\.?',
]

COAST_PATTERNS = [
ur'(?u)(\d+)\s*(у\.?\s*е\.?)/?\s*(месяц)?\.?',					 #300 у. е. 600уе
ur'(?u)(\d+)\s*(грн?\.?)\s*/?\s*(месяц)?\.?'			 #3000 грн/ месяц.  
]

FLAT_SQUARE_PATTERNS = [
ur'(?u)(\d+)\s*м\.?\s*к?в?\.?',					 #36 м. кв.						
]
#4 цена -> пер ГерЦЕНА
#5 новая -> ЗерНОВАЯ
STREET_MIN_CHAR_COUNT = 5
STREET_PATTERNS = [
ur'(?u)([а-яА-Я]{%d,})\s*[а-яА-Я]*\s*/\s*([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT, STREET_MIN_CHAR_COUNT), # Not sure about this
ur'(?u)([а-яА-Я]{%d,})\s*\s*/\s*([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT, STREET_MIN_CHAR_COUNT),
ur'(?u)([а-яА-Я]{%d,})\s*,\s*([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT, STREET_MIN_CHAR_COUNT),
ur'(?u)([а-яА-Я]{%d,})' % (STREET_MIN_CHAR_COUNT),
]

TELEPHONE_MATCHER = BaseMatcher(TELEPHONE_PATTERNS, 'telphones', foundEntitiesLimit = -1)
ROOM_COUNT_MATCHER = BaseMatcher(ROOM_COUNT_PATTERNS, 'room count')
COAST_MATCHER = BaseMatcher(COAST_PATTERNS, 'coast')
FLAT_SQUARE_MATCHER = BaseMatcher(FLAT_SQUARE_PATTERNS, 'flat square')
STREET_MATCHER = StreetMatcher(STREET_PATTERNS, 'street')
#ADDRESS_MATCHER = AddressMatcher()

def dispatchCoast(result_set):
	if len(result_set) != 3:
		raise ValueError, 'Should be three values in result set: %s' % result_set
	coast, currency, period = result_set 
	#coast = int(coast)
	#currency = currency.replace(' ', '')#.replace('.', '')
	if not period:
		period = u''
	result = {}
	result[u'value'] = coast
	result[u'currency'] = currency
	result[u'period'] = period
	return result

def dispatchOneInt(result_set):
	if len(result_set) != 1:
		raise ValueError, 'Should be one value in result set: %s' % result_set
	return int(result_set.pop())

def dispatchRoomCount(result_set):
	return dispatchOneInt(result_set)

def dispatchSquare(result_set):
	return dispatchOneInt(result_set)

def dispatchAddress(result_set):
	result = {}
	if len(result_set) == 2:
		result[u'street1'] = result_set.pop(False)
		result[u'street2'] = result_set.pop(False)
	else:
		result[u'street1'] = result_set.pop()
	return result

def findCoast(input):
	(result_set, updated_input) = COAST_MATCHER.match(input)
	return dispatchCoast(result_set)

def findRoomCount(input):
	(result_set, updated_input) = ROOM_COUNT_MATCHER.match(input)
	return dispatchRoomCount(result_set)

def findPhoneNumbers(input):
	(result_set, updated_input) = TELEPHONE_MATCHER.match(input)
	return result_set

def findAddress(input):
	(result_set, updated_input) = STREET_MATCHER.match(input)
	return dispatchAddress(result_set)