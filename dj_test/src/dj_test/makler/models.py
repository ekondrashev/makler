from django.db import models

class Street(models.Model):
    name = models.CharField(max_length=50)

class StreetFreak(models.Model):
    street = models.ForeignKey(Street)
    name = models.CharField(max_length=50)

class Address(models.Model):
    street = models.ForeignKey(Street, related_name = "street")
    corner_street = models.ForeignKey(Street, related_name = "corner_street")
    number = models.CharField(max_length=10)

class Flat(models.Model):
    address = models.ForeignKey(Address)
    type = models.CharField(max_length=50)#Stalinka, etc
    total_square = models.IntegerField()
    room_count = models.IntegerField()

class Room(models.Model):
    flat = models.ForeignKey(Flat)
    square = models.IntegerField()

class Lease(models.Model):
    flat = models.ForeignKey(Flat)
    price = models.IntegerField()
    period = models.CharField(max_length=50)
    comments = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

