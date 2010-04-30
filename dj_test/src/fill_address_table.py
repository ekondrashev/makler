# -*- coding: utf-8 -*- 
'''
Created on 21.04.2010

@author: ekondrashev
'''
import os

ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"
os.environ[ENVIRONMENT_VARIABLE] = 'dj_test.settings'
import csv
import codecs
import logging

from dj_test.makler.models import Address, Street

DELETE_OLD_RECORDS = True

TARGET_CITY = u'Одесса'
TARGET_TXT_FILE = 'streets.txt'
TARGET_CSV_FILE = 'streets.csv'
STREET_FREAKS = {
'Нежинская' : ['Неженская'],
}

logging.basicConfig(level=logging.DEBUG)

def csv_to_txt():
    reader = csv.reader(codecs.open(TARGET_CSV_FILE, "r", "cp1251"))
    target_file = codecs.open(TARGET_TXT_FILE, "w", "utf-8" )
    for row in reader:
        for r in row:
            city, street_name, street_number = r.split(';')
            if city == TARGET_CITY:
                target_file.write("%s;%s\n" % (street_name, street_number))

def deleteAddressRecords():
    logging.debug('Deleting all existing Address records')
    Address.objects.all().delete()
    logging.debug('Deleting done')

def txt_to_db():
    if DELETE_OLD_RECORDS:
        deleteAddressRecords()
    target_file = open(TARGET_TXT_FILE, "r")
    lines = target_file.read().split('\n')
    added_streets = {}
    for line in lines:
        if line.find(';') < 0:
            continue
        street_name, street_number = line.split(';')
        logging.debug('Saving.. %s %s' % (street_name, street_number))
        if not added_streets.has_key(street_name):
            street = Street(name = street_name)
            street.save()
            added_streets[street_name] = street
        else:
            logging.debug('Street already added: %s' % (street_name))
            street = added_streets[street_name]

        address = Address(street = street, corner_street = street, number = street_number)
        address.save()

if __name__ == '__main__':
	code the street freaks!!
    csv_to_txt()
    txt_to_db()
