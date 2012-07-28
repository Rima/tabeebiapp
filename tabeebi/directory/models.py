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


class Location(models.Model):
    country = models.IntegerField( choices=COUNTRIES )
    city = models.IntegerField( choices=CITIES )

    address = models.CharField( max_length=255 )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField( null=True, blank=True )

    def basic_dict(self):
        return { 'country' : self.get_country_display(), 'city' : self.get_city_display(),
                 'address' : self.address , 'latitude' : self.latitude, 'longitude' : self.longitude }

    def __unicode__(self):
        return "%s - %s - %s" % ( self.get_country_display(), self.get_city_display(), self.address )



class Provider(models.Model):
    name = models.CharField( max_length=255 )
    type = models.IntegerField( choices=TYPES )
    location = models.ForeignKey(Location)
    networks_categories = models.ManyToManyField(NetworkCategory)

    telephone = models.CharField( max_length=255 )
    fax = models.CharField(max_length=255, null=True, blank=True )
    pobox = models.CharField( max_length=7, null=True, blank=True )

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
        }

    def __unicode__(self):
        return self.name



