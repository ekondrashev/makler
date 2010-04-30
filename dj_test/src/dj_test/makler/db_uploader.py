# -*- coding: utf-8 -*-
'''
Created on 19.04.2010

@author: ekondrashev
'''

import os
import re
import codecs
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'

#from dj_test.makler.models import Address, Flat, Lease, Room


DELIMITER = "Подробнее..."

TELEPHONE_REG = u'([0-9]*\-?\ ?)*'
TELEPHONE = re.compile(TELEPHONE_REG, re.UNICODE)


if __name__ == '__main__':
    '''
    input = codecs.open("test.input", "r", "cp1251")
    text = input.read().decode('utf-8')
    print text
    declarations = text.split(DELIMITER)  
    print 'Declarations count = %s' % (len(declarations))
    for decl in declarations:
        match = TELEPHONE.search(decl, re.UNICODE)
        if match:
            print match.groups()
        else:
            print 'No telephone found'

    print "Тест"
    input.close()
    '''
    match = re.search(TELEPHONE_REG, u"Телефон: 0677401733, 0505523474, 0939120441, 7004516", re.UNICODE)
    if match:
        print match.groups()
    else:
        print 'No match'
    