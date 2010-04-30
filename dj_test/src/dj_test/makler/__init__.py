# -*- coding: utf-8 -*- 

from dj_test.makler.parser.matcher import BaseMatcher

TELEPHONE_PATTERNS = [ 
ur'(?u)(8?0\d{2}\s?\-?\s?\d{3}\s?\-?\s?\d{2}\s?\-?\s?\d{2})' ,#0677401733, 050 552 34 74, 22, 093-912-04-41,
ur'(?u)(\d{3}\s?\-?\s?\d{2}\s?\-?\s?\d{2})',  #700 45 16, 700 - 45 - 16
ur'(?u)(\d{7})', #7004516
]

#Возвращаемый результат один 
ROOM_COUNT_PATTERNS = [
ur'(?u)(\d+)\s*-?\s*х?\s*ком\.?\s*квартиру',     #2- х ком. квартиру, 1 ком квартиру
ur'(?u)(\d+)\s*комн\.?\s*(?:\w+\.?)?\s*кв\.?',   #4 комн самост. кв. #самост???
ur'(?u)(\d+)\s*-?\s*к\.?\s*к?в?\.?',             #1- к, 4 к кв
#u'(\d+) ком\.? кв\.?',
#u'(\d+)\s*-\s*к\.?',    #1-к
#u'(\d+) комн\.?',
]

COAST_PATTERNS = [
ur'(?u)(\d+)\s*(у\.?\s*е\.?)/?\s*(месяц)?\.?',                     #300 у. е. 600уе
ur'(?u)(\d+)\s*(грн)\s*/?\s*(месяц)?\.?'             #3000 грн/ месяц.  
]

FLAT_SQUARE_PATTERNS = [
ur'(?u)(\d+)\s*м\.?\s*к?в?\.?',                     #36 м. кв.                        
]


TELEPHONE_MATCHER = BaseMatcher(TELEPHONE_PATTERNS, 'telphones')
ROOM_COUNT_MATCHER = BaseMatcher(ROOM_COUNT_PATTERNS, 'room count')
COAST_MATCHER = BaseMatcher(COAST_PATTERNS, 'coast')
FLAT_SQUARE_MATCHER = BaseMatcher(FLAT_SQUARE_PATTERNS, 'flat square')
#ADDRESS_MATCHER = AddressMatcher()

def dispatchCoast(result_set):
    if len(result_set) != 3:
        raise ValueError, 'Should be three values in result set: %s' % result_set
    coast, currency, duration = result_set 
    coast = int(coast)
    currency = currency.replace(' ', '').replace('.', '')
    if not duration:
        duration = ''
    return coast, currency, duration

def dispatchOneInt(result_set):
    if len(result_set) != 1:
        raise ValueError, 'Should be one value in result set: %s' % result_set
    return int(result_set.pop())

def dispatchRoomCount(result_set):
    return dispatchOneInt(result_set)

def dispatchSquare(result_set):
    return dispatchOneInt(result_set)