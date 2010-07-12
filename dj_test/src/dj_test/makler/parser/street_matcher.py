# -*- coding: utf-8 -*- 
'''
Created on 28.04.2010

@author: ekondrashev
'''
import os
import logging
import aspects
from dj_test.makler.utils import OrderedSet

from dj_test.makler.parser.matcher import BaseMatcher, baseMatcher_cut_log,\
    baseMatcher_match_log
from dj_test.makler.models import Street, StreetFreak

logging.basicConfig(level=logging.DEBUG)

ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'



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

aspects.with_wrap(baseMatcher_match_log, StreetMatcher.match)
aspects.with_wrap(baseMatcher_cut_log, StreetMatcher.cut)
aspects.with_wrap(streetMatcher_find_street, StreetMatcher.findStreet)
aspects.with_wrap(streetMatcher__matchWithoutCut, StreetMatcher._matchWithoutCut)