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
    #alter table directory_country add column iso_code varchar(6);
    iso_code = models.CharField(max_length=5)

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)
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

        addresses = [self.address1, self.address2, self.address3, self.address4]

        return { 'country' : self.country.name, 'city' : self.city.name,
                 'addresses' : addresses,
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


            "other":[{"fieldname":"mobile phone",
                      "fieldvalue":"0936726827"},
                    {"fieldname":"work days",
                     "fieldvalue":" Mon till Thu"},
                    {"fieldname":"Emergency",
                     "fieldvalue":"YES"}]
        }

    def __unicode__(self):
        return self.name


class FrequentlyAskedQuestion(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __unicode__(self):
        return self.question

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


#choices: provider_type
from django.db.models.fields import NullBooleanField
class ProviderFullDetails(models.Model):
    provider_name = models.CharField(max_length=255)
    provider_type = models.IntegerField( choices=TYPES )

    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    location = models.TextField()
    area = models.CharField(max_length=255, null=True, blank=True)

    telephone = models.CharField(max_length=255)
    fax = models.CharField(max_length=255)

    pobox = models.CharField(max_length=255)

    daman_global = models.NullBooleanField()
    daman_international = models.NullBooleanField()
    daman_regional = models.NullBooleanField()
    dubaicare_n1 = models.NullBooleanField()
    dubaicare_n2 = models.NullBooleanField()
    dubaicare_n3 = models.NullBooleanField()
    dubaicare_n4 = models.NullBooleanField()
    nextcare_gn = models.NullBooleanField()
    nextcare_rn = models.NullBooleanField()
    nextcare_rn2 = models.NullBooleanField()
    mednet_gold = models.NullBooleanField()
    mednet_silver_premium = models.NullBooleanField()
    mednet_green = models.NullBooleanField()
    nowhealth = models.NullBooleanField()
    nas_comprehensive = models.NullBooleanField()
    nas_rn = models.NullBooleanField()
    nas_srn = models.NullBooleanField()
    metlife_alico_vip = models.NullBooleanField()
    metlife_alico_gold = models.NullBooleanField()
    metlife_alico_standard_silver = models.NullBooleanField()
    metlife_alico_limited_blue = models.NullBooleanField()
    metlife_alico_restricted_green = models.NullBooleanField()


    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    NETWORK_INDEX_FIELD_MAP = {
        1 : 'daman_global',
        2 : 'daman_international',
        3 : 'daman_regional',
        4 : 'dubaicare_n1',
        5 : 'dubaicare_n2',
        6 : 'dubaicare_n3',
        7 : 'dubaicare_n4',
        8 : 'nextcare_gn',
        9 : 'nextcare_rn',
        10 : 'nextcare_rn2',
        11 : 'mednet_gold',
        12 : 'mednet_silver_premium',
        13 : 'mednet_green',
        14 : 'nowhealth',
        15 : 'nas_comprehensive',
        16 : 'nas_rn',
        17 : 'nas_srn',
        18 : 'metlife_alico_vip',
        19 : 'metlife_alico_gold',
        20 : 'metlife_alico_standard_silver',
        21 : 'metlife_alico_limited_blue',
        22 : 'metlife_alico_restricted_green',
    }

    def __unicode__(self):
        return self.provider_name

    def networks(self):
        #for self boolean fields. list true ones.
        res = []
        for fld in self._meta.fields:
            if isinstance(fld, NullBooleanField) and getattr(self, fld.name):
                res.append( fld.verbose_name )
        return res

    def location_data(self):
        return {
            'area' : self.area,
            'address' : self.location,
            'latitude' : self.latitude,
            'longitude' : self.longitude,
            'city' : self.city,
            'country' : self.country
        }

    def to_json(self):
        return {
            'name' : self.provider_name,
            'location' : self.location_data(),
            'type' : self.get_provider_type_display(),
            'networks_categories' : self.networks(),
            'telephone' : self.telephone,
            'fax' : self.fax,
            'pobox' : self.pobox,
            #'website' : self.website,
            #'email' : self.email,
            'distance' : '',


            "other":[{"fieldname":"work days",
                     "fieldvalue":" Mon till Thu"},
                    {"fieldname":"Emergency",
                     "fieldvalue":"YES"}],

            "other_contacts": [
                    {"fieldname":"mobile phone",
                     "fieldvalue":"0936726827"},
            ]
        }
