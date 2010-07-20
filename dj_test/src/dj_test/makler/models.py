from django.db import models

class Street(models.Model):
    UNKNOWN_STREET_NAME='UNKNOWN'
    name = models.CharField(max_length=50)
    @staticmethod
    def getUnknownStreet():
        try:
            unknown = Street.objects.get(name=Street.UNKNOWN_STREET_NAME)
        except Street.DoesNotExist:
            unknown = Street(name=Street.UNKNOWN_STREET_NAME)
            unknown.save()
        return unknown


class StreetFreak(models.Model):
    street = models.ForeignKey(Street)
    name = models.CharField(max_length=50)

class Address(models.Model):
    street = models.ForeignKey(Street, related_name = "street", default=Street.getUnknownStreet())
    corner_street = models.ForeignKey(Street, related_name = "corner_street", default=Street.getUnknownStreet())
    number = models.CharField(max_length=10)

class Flat(models.Model):
    address = models.ForeignKey(Address)
    type = models.CharField(max_length=50)#Stalinka, etc
    total_square = models.IntegerField()
    room_count = models.IntegerField()

class Room(models.Model):
    flat = models.ForeignKey(Flat)
    square = models.IntegerField()

class Advertisement(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now=True)

class Lease(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    flat = models.ForeignKey(Flat)
    price = models.FloatField()
    currency = models.CharField(max_length=10)
    period = models.CharField(max_length=50)

class Makler(models.Model):
    name = models.CharField(max_length=20)
    UNKNOWN_MAKLER_NAME = 'UNKNOWN'
    @staticmethod
    def getUnknownMakler():
        try:
            unknown = Makler.objects.get(name=Makler.UNKNOWN_MAKLER_NAME)
        except Makler.DoesNotExist:
            unknown = Makler(name=Makler.UNKNOWN_MAKLER_NAME)
            unknown.save()
        return unknown
        
class PhoneNumber(models.Model):
    number = models.CharField(max_length=10)
    lease = models.ForeignKey(Lease)
    makler = models.ForeignKey(Makler, default=Makler.getUnknownMakler())
    