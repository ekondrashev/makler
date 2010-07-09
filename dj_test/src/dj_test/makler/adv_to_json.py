# -*- coding: utf-8 -*- 
import json
import logging
import traceback
import sys
from dj_test.makler import findRoomCount, findCoast, findPhoneNumbers, findAddress

logging.basicConfig(level=logging.DEBUG)

PARSING_ENTITIES = {
'roomCount' : findRoomCount,
'cost' : findCoast,
'phoneNumbers' : findPhoneNumbers,
'address' : findAddress,
}
def getJson(adv):
    result = {}
    for entity, finder in PARSING_ENTITIES.iteritems():
        foundValue = ''
        try:
            foundValue = finder(adv)
        except Exception, ex:
            traceback.print_exc(file=sys.stdout)
            logging.debug(ex)
        result[entity] = foundValue
    json_str = json.dumps(result)
    logging.debug(json_str)
    return json_str

if __name__ == "__main__":
    adv = u'Сдам 2х Неженская, Евроремонт, 300у. е., 36 м. кв., бель/ 2, Евроремонт, пустая, хорошая транспортная развязка, рядом универсам Таврия. 300у. е. Телефон: 063 306 03 15'
    adv1 =unicode("""%D0%A1%D0%B4%D0%B0%D0%BC%202%D1%85%20%D0%9D%D0%B5%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B0%D1%8F,%20%D0%95%D0%B2%D1%80%D0%BE%D1%80%D0%B5%D0%BC%D0%BE%D0%BD%D1%82,%20300%D1%83.%20%D0%B5.,%2036%20%D0%BC.%20%D0%BA%D0%B2.,%20%D0%B1%D0%B5%D0%BB%D1%8C/%202,%20%D0%95%D0%B2%D1%80%D0%BE%D1%80%D0%B5%D0%BC%D0%BE%D0%BD%D1%82,%20%D0%BF%D1%83%D1%81%D1%82%D0%B0%D1%8F,%20%D1%85%D0%BE%D1%80%D0%BE%D1%88%D0%B0%D1%8F%20%D1%82%D1%80%D0%B0%D0%BD%D1%81%D0%BF%D0%BE%D1%80%D1%82%D0%BD%D0%B0%D1%8F%20%D1%80%D0%B0%D0%B7%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0,%20%D1%80%D1%8F%D0%B4%D0%BE%D0%BC%20%D1%83%D0%BD%D0%B8%D0%B2%D0%B5%D1%80%D1%81%D0%B0%D0%BC%20%D0%A2%D0%B0%D0%B2%D1%80%D0%B8%D1%8F.%20300%D1%83.%20%D0%B5.%20%D0%A2%D0%B5%D0%BB%D0%B5%D1%84%D0%BE%D0%BD:%20063%20306%2003%2015""")
    getJson(adv1)
    #getJson(u'addsa 2х')