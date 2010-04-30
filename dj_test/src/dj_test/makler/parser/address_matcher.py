# -*- coding: utf-8 -*- 
'''
Created on 22.04.2010

@author: ekondrashev
'''
import os

ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'

from dj_test.makler.parser.matcher import BaseMatcher
from dj_test.makler.models import Street

class AddressMatcher(BaseMatcher):
    def match(self, input):
        return BaseMatcher.match(self, input)

if __name__ == '__main__':
    input = u'Сдам 1 ком. кв. Тополева / Королева. 3/10эт. 57м – общая. Евроремонт. 2 лоджии застеклены. Гардеробная. Стеклопакеты. Импортная мебель, встроенная кухня. Вся бытовая техника. Тамбур. На длительный срок. 500у. е.'
    patterns = [ur'(?u)([а-яА-Я]+)\s*/\s*([а-яА-Я]+)']
    matcher = BaseMatcher(patterns, 'street')
    street_name, corner_street_name = matcher.match(input)[0]
    print street_name, corner_street_name
    print Street.objects.all()
    street = Street.objects.filter(name__contains=street_name)[0]
    corner_street = Street.objects.filter(name__contains=corner_street_name)[0]
    print street.name, corner_street.name
    