from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from tabeebi.directory import CITIES_CHOICES, TYPES_MATCH
from tabeebi.directory.helper import queryset_iterator
from tabeebi.directory.models import *
from django.utils.simplejson import dumps
from django.core.cache import cache

from django.core.serializers import serialize

def serializer(request):

    AVAILABLE_MODELS = {
        'Directory' : Provider,
        }

    type = request.GET.get("type", "json")
    model_name = request.GET.get("model", "Directory")
    limit = request.GET.get("limit", 10)
    fields = request.GET.get("fields", None)
    if not fields:
        fields = ('id',)
    else:
        fields = tuple(fields.split(","))

    #do some checks on data
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    else:
        if limit > 200: limit=10
    if model_name not in AVAILABLE_MODELS.keys():
        raise Http404
    if type not in ("json", "xml"): type="json"


    model = AVAILABLE_MODELS[model_name]

    filters = {}

    data = model.objects.filter( **filters )[:limit]
    j_data = { 'providers' : [ item.to_json() for item in data ]}
    return HttpResponse( dumps( j_data ) )


def data_states(request):
    states = DataState.objects.all()

    results = {}

    for item in states:
        results.update({item.name : {'version' : item.version, 'enabled' : item.enable}  })

    return HttpResponse(dumps(results),
        content_type='application/json')


def countries_cities_list(request):
    countries = Country.objects.all()
    results = []

    for country in countries:
        cities = list(country.city_set.values('id', 'name'))
        results.append( {"id": country.id ,"name": country.name, "cities": cities  } )

    return HttpResponse(dumps(results),
        content_type='application/json')


def insurance_companies(request):
    categories = NetworkCategory.objects.all()

    results = []
    for cat in categories:
        results.append({ 'id' : cat.id, 'name' : '%s - %s' % (cat.network, cat.category) })

    return HttpResponse(dumps(results),
            content_type='application/json')


def providers_list(request):

    cache_key = "providers_list"


    type = request.GET.get('type', None)
    city = request.GET.get('city', None)
    country = request.GET.get('country', None)
    longitude = request.GET.get('longitude', '')
    latitude = request.GET.get('latitude', '')
    networks = request.GET.get('networks', None)

    if networks:
        networks = networks.split(',')


    kwargs = {}
    if city:
        kwargs.update({ 'location__city_id' : city })
        cache_key = "%s_%s" % (cache_key , city)
    if country:
        kwargs.update({ 'location__country_id' : country })
        cache_key = "%s_%s" % (cache_key , country)
    if networks:
        kwargs.update({ 'networks_categories__id__in' : networks })
        cache_key = "%s_%s" % (cache_key , networks)
    if type:
        kwargs.update({ 'type' : int(type) })
        cache_key = "%s_%s" % (cache_key , type)

    results = cache.get(cache_key)

    if not results:
        if kwargs:
            providers = Provider.objects.filter(**kwargs)
        else:
            providers = Provider.objects.all()

        results = []
        for provider in providers:
            results.append(provider.to_json())

        cache.set(cache_key, results)

    return HttpResponse(dumps(results),
        content_type='application/json')


@login_required
def store_countries_networks_cities(request):

    #get countries
    countries = FlatTable.objects.values('country').distinct()

    for country in countries:
        cntr = Country(name=country['country'])
        cntr.save()

        #get cities
        #dont' forget to manually clean this list from none cities
        cities = FlatTable.objects.filter(country=country['country']).values('city').distinct()
        for city in cities:
            City.objects.create(name=city['city'], country=cntr)




    #store insurance network names
    networks = FlatTable.objects.values('insurance_name').distinct()
    for network in networks:
        netw = Network(name=network['insurance_name'])
        netw.save()

        #store insurance network categories
        categories = FlatTable.objects.filter(insurance_name=network['insurance_name']).values('network').distinct()
        for category in categories:
            NetworkCategory.objects.create(category=category['network'], network=netw)

    return HttpResponse("data refreshed")


@login_required
def store_data_in_places(request):

    #store provider
    #for each provider -
    # try to find a provider with a similar name - if found, add to location, add to network categories.
    # if not: match their country, city, create location object and add to network categories

    for provider in queryset_iterator(FlatTable.objects.all()):
        #try to find a provider with a similar name
        exists = Provider.objects.filter(name__icontains=provider.provider)
        if len(exists):
            #add to location
            outlet = exists[0]
            outlet.location.address3 = provider.location1
            outlet.location.address4 = provider.location2
            outlet.location.save()
            #add to networks
            insurance = Network.objects.filter(name=provider.insurance_name)[0]
            network = NetworkCategory.objects.filter(network=insurance, category=provider.network)
            if len(network):
                outlet.networks_categories.add(network[0])
        else:
            #create it
            provider_country = Country.objects.get(name=provider.country)
            location = Location(country=provider_country, address1=provider.location1, address2=provider.location2)

            provider_city = City.objects.filter(name=provider.city)
            if provider_city: location.city = provider_city[0]
            location.save()

            provider_type = TYPES_MATCH[provider.type.lower()]

            insurance = Network.objects.filter(name=provider.insurance_name)[0]
            network = NetworkCategory.objects.filter(network=insurance, category=provider.network)

            outlet = Provider(name=provider.provider, location=location, telephone=provider.telephone, fax=provider.fax,
                pobox=provider.pobox, type=provider_type)
            outlet.save()

            if len(network):
                outlet.networks_categories.add(network[0])


    return HttpResponse("data refreshed")




def faq(request):
    results = list(FrequentlyAskedQuestion.objects.values('question', 'answer'))

    return HttpResponse(dumps(results),
        content_type='application/json')



