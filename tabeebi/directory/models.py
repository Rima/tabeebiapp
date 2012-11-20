from django.db import models
from tabeebi.directory import COUNTRIES, CITIES, TYPES


class Network(models.Model):
    name = models.CharField( max_length=255 )

    def __unicode__(self):
        return self.name

class NetworkCategory(models.Model):
    network = models.ForeignKey(Network)
    category = models.CharField( max_length=15 )

    def basic_dict(self):
        return { 'network' : self.network.name, 'category' : self.category }

    def __unicode__(self):
        return self.category


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

class Location(models.Model):
    country = models.ForeignKey(Country)
    city = models.ForeignKey(City, null=True, blank=True)

    address1 = models.CharField( max_length=255 )
    address2 = models.CharField( max_length=255 )
    address3 = models.CharField( max_length=255 )
    address4 = models.CharField( max_length=255 )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField( null=True, blank=True )

    def basic_dict(self):
        return { 'country' : self.country.name, 'city' : self.city.name,
                 'address1' : self.address1, 'address2' : self.address2,
                 'address3' : self.address3, 'address4' : self.address4,
                 'latitude' : self.latitude, 'longitude' : self.longitude }

    def __unicode__(self):
        return "%s - %s - %s" % ( self.country.name, self.city.name, self.address1 )



class Provider(models.Model):
    name = models.CharField( max_length=255 )
    type = models.IntegerField( choices=TYPES )
    location = models.ForeignKey(Location)
    networks_categories = models.ManyToManyField(NetworkCategory)

    telephone = models.CharField( max_length=255 )
    fax = models.CharField(max_length=255, null=True, blank=True )
    pobox = models.CharField( max_length=100, null=True, blank=True )

    website = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)

    def to_json(self, fields=(id,name,location)):
        return {
            'name' : self.name,
            'location' : self.location.basic_dict(),
            'type' : self.get_type_display(),
            'networks_categories' : [ nc.basic_dict() for nc in self.networks_categories.all() ],
            'telephone' : self.telephone,
            'fax' : self.fax,
            'pobox' : self.pobox,
            'website' : self.website,
            'email' : self.email,
            'distance' : '',
        }

    def __unicode__(self):
        return self.name



class DataState(models.Model):
    name = models.CharField(max_length=255)
    version = models.PositiveSmallIntegerField()
    enable = models.NullBooleanField()

    def __unicode__(self):
        return self.name



class FlatTable(models.Model):
    provider = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pobox = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)
    location1 = models.CharField(max_length=400)
    location2 = models.CharField(max_length=400)

    insurance_name = models.CharField(max_length=255)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


