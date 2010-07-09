'''
Created on 08.07.2010

@author: ekondrashev
'''

from dj_test.makler.models import Address, Advertisement, Flat, Lease, Street, StreetFreak
from django.contrib import admin

admin.site.register(Address)
admin.site.register(Advertisement)
admin.site.register(Flat)
admin.site.register(Lease)
admin.site.register(Street)
admin.site.register(StreetFreak)
