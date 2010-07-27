# -*- coding: utf-8 -*- 
'''
Created on 21.04.2010

@author: ekondrashev
'''
import os
import logging
import re
from dj_test.makler.utils import collection_str

logging.basicConfig(level=logging.DEBUG)
ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'

def baseMatcher_cut_log(func):
    def wrapper(*args, **kwargs):
        baseMatcher = args[0]
        match = args[1]
        logging.debug('%s:pattern: %s pretender: %s' % (baseMatcher.lookingEntityName, match.re.pattern, collection_str(match.groups())))
        #logging.debug('Found pretender to %s: %s' % (baseMatcher.lookingEntityName, collection_str(match.groups())))
        return func(*args, **kwargs)
    return wrapper

def baseMatcher_match_log(func):
    def wrapper(*args, **kwargs):
        baseMatcher = args[0]
        input = args[1]
        logging.debug('                --------------- %s: started --------------- ' % baseMatcher.lookingEntityName)
        logging.debug('Original input: %s' % input)
        retval = func(*args, **kwargs)
        logging.debug('--------------- ----------------------------------- --------------- ')
        length = len(retval[0])
        if not length:
            logging.debug('No %s found' % baseMatcher.lookingEntityName)
        else:
            logging.debug('Found %s %s: %s' % (length, baseMatcher.lookingEntityName, collection_str(retval[0])))
        logging.debug('Updated input: %s' % retval[1])
        logging.debug('                --------------- %s: ended --------------- ' % baseMatcher.lookingEntityName)
        return retval
    return wrapper

def baseMatcher_matchWithCut_log(func):
    def wrapper(*args, **kwargs):
        input = args[1]
        pattern = args[2].pattern
        logging.debug('--------------------')
        logging.debug('Applying pattern : %s' % (pattern))
        logging.debug('For input: %s' % (input))
        logging.debug('--------------------')
        return  func(*args, **kwargs)
    return wrapper

class BaseMatcher(object):
    '''
    classdocs
    '''

    def __init__(self, patterns_str, lookingEntityName, replaceMatches = True, replacementString = '', foundEntitiesLimit = 1):
        self.patterns = []
        for p in patterns_str:
            self.patterns.append(re.compile(p))
        self.foundEntities = []
        self.lookingEntityName = lookingEntityName.upper()
        self.replaceMatches = replaceMatches
        self.replacementString = replacementString
        self.foundEntitiesLimit = foundEntitiesLimit

    @baseMatcher_cut_log
    def cut(self, match):
        for i in range(0,len(match.groups())):
            self.foundEntities.append(match.group(i+1))
        #self.foundEntities.add(match.group(1))
        return self.replacementString

    @baseMatcher_matchWithCut_log
    def _matchWithCut(self, input, pattern):
        limit = self.foundEntitiesLimit
        if self.foundEntitiesLimit < 0:
            limit += 1
        return pattern.sub(self.cut, input, limit)

    #@streetMatcher__matchWithoutCut
    def _matchWithoutCut(self, input, pattern):
        self.foundEntities.extend(pattern.findall(input))
        return input

    @baseMatcher_match_log
    def match(self, input):
        self.foundEntities = []
        if self.replaceMatches:
            in_match = self._matchWithCut
        else:
            in_match = self._matchWithoutCut

        for pattern in self.patterns:
            input = in_match(input, pattern)
            if len(self.foundEntities) == self.foundEntitiesLimit:
                break
        return (self.foundEntities, input)

PATTERNS = [
u'(\d+)\s*-\s*х ком\.?квартиру',     #2- х ком. квартиру
u'(\d+) ком\.? кв\.?',
u'(\d+) к\.? кв\.?',
u'(\d+) комн\.? кв\.?',
u'(\d+)\s*-\s*к\.?',    #1-к
u'(\d+) комн\.?',
]

if __name__ == '__main__':
    input = u"Сдам 1- к на Довженко"
    matcher = BaseMatcher(PATTERNS, 'room count')        
    matcher.match(input)
