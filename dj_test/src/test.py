#!/usr/bin/python 
# -*- coding: utf-8 -*- 

import re

def matched(match):
    print match.group(1)
    return ''
'''
s=u"Привет мир!!!";
print s

hello_pattern = re.compile( u'([пП]ривет \w*)', re.UNICODE )

r = hello_pattern.search( s )
print r.group(0);

match = re.search(u'([0-9]*\-?\ ?)*', u"Телефон: 0677401733, 0505523474, 0939120441, 7004516", re.UNICODE)
if match:
    print match.groups()
else:
    print 'No match'
'''
    
p1 = ur'(?u)(\d+)\s*м\.?\s*к?в?\.?' 
str = u'36 м. кв., бель/ 2, Евроремонт, пустая, '
print re.findall(p1, str)
print re.sub(p1, matched, str)


s1, s2 = 'фыв', 'фыв' 
print [s1, s2]

s1, s2 = '%s'%'фыв', '%s'%'фыв' 
print [s1, s2]
print type('выф')


