# -*- coding: utf-8 -*- 
'''
Created on 21.04.2010

@author: ekondrashev
'''
import logging
import re
import aspects
from dj_test.makler.utils import collection_str

logging.basicConfig(level=logging.DEBUG)

class BaseMatcher(object):
    '''
    classdocs
    '''

    def __init__(self, patterns_str, lookingEntityName, replaceMatches = True, replacementString = ''):
        self.patterns = []
        for p in patterns_str:
            self.patterns.append(re.compile(p))
        self.foundEntities = []
        self.lookingEntityName = lookingEntityName.upper()
        self.replaceMatches = replaceMatches
        self.replacementString = replacementString

    def cut(self, match):
        for i in range(0,len(match.groups())):
            self.foundEntities.append(match.group(i+1))
        #self.foundEntities.add(match.group(1))
        return self.replacementString

    def _matchWithCut(self, input, pattern):
        return pattern.sub(self.cut, input, 1)
    
    def _matchWithoutCut(self, input, pattern):
        self.foundEntities.extend(pattern.findall(input))
        return input

    def match(self, input):
        self.foundEntities = []
        if self.replaceMatches:
            in_match = self._matchWithCut
        else:
            in_match = self._matchWithoutCut

        for pattern in self.patterns:
            input = in_match(input, pattern)
            if self.foundEntities:
                break
        return (self.foundEntities, input)

def baseMatcher_cut_log(*args, **kwargs):
    baseMatcher = args[0]
    match = args[1]
    logging.debug('%s:pattern: %s pretender: %s' % (baseMatcher.lookingEntityName, match.re.pattern, collection_str(match.groups())))
    #logging.debug('Found pretender to %s: %s' % (baseMatcher.lookingEntityName, collection_str(match.groups())))
    retval = yield aspects.proceed(*args, **kwargs)
    yield aspects.return_stop(retval)

def baseMatcher_match_log(*args, **kwargs):
    baseMatcher = args[0]
    input = args[1]
    logging.debug('				--------------- %s: started --------------- ' % baseMatcher.lookingEntityName)
    logging.debug('Original input: %s' % input)
    retval = yield aspects.proceed(*args, **kwargs)
    logging.debug('--------------- ----------------------------------- --------------- ')
    length = len(retval[0]) 
    if not length:
        logging.debug('No %s found' % baseMatcher.lookingEntityName)
    else:
        logging.debug('Found %s %s: %s' % (length, baseMatcher.lookingEntityName, collection_str(retval[0])))
    logging.debug('Updated input: %s' % retval[1])
    logging.debug('				--------------- %s: ended --------------- ' % baseMatcher.lookingEntityName)
    yield aspects.return_stop(retval)

def baseMatcher_matchWithCut_log(*args, **kwargs):
    input = args[1]
    pattern = args[2].pattern
    logging.debug('--------------------')
    logging.debug('Applying pattern : %s' % (pattern))
    logging.debug('For input: %s' % (input))
    logging.debug('--------------------')
    retval = yield aspects.proceed(*args, **kwargs)
    yield aspects.return_stop(retval)
    
aspects.with_wrap(baseMatcher_cut_log, BaseMatcher.cut)
aspects.with_wrap(baseMatcher_match_log, BaseMatcher.match)
aspects.with_wrap(baseMatcher_matchWithCut_log, BaseMatcher._matchWithCut)


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
    
    
    
    