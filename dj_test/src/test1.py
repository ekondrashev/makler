'''
Created on 20.04.2010

@author: ekondrashev
'''
import re

p1 = '(8?0\d{2}\s?\-?\d{3}\s?\-?\d{2}\s?\-?\d{2})'#0677401733, 050 552 34 74, 22, 093-912-04-41
#Dummy workaround with .* need to fix
p2 = '.*(\d{3}\s?\d{2}\s?\d{2})' #700 45 16
p3 = '.*(\d{7})' #7004516
if __name__ == '__main__':
    s1, s2 = 'ôûâ', 'ôûâ' 
    print [s1, s2]
    print type('âûô')

    input = "0677401733, 050 552 34 74, 22, 093-912-04-41, 0939120441, 7004516, 700 45 16"
    print re.sub(p1, input, '')
    print re.findall(p2, input)
    print re.findall(p3, input)
