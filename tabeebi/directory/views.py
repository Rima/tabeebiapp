from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
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


def provider_types_list(request):

    results = TYPES

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

import operator
def providers_list(request):

    cache_key = "providers_list"

    number_per_page = 20

    query = request.GET.get('query', None)
    type = request.GET.get('type', None)
    city = request.GET.get('city', None)
    country = request.GET.get('country', None)
    longitude = request.GET.get('longitude', '')
    latitude = request.GET.get('latitude', '')
    networks = request.GET.get('networks', None)

    if networks:
        networks = networks.split(',')


    kwargs = {}
    query_args = []
    if query:
        query = query.strip()
        kw_tag_qs = (Q(location__address1__icontains=query) |
                                            Q( location__address2__icontains=query) |
                                            Q( location__address3__icontains=query) |
                                            Q( location__address4__icontains=query) |
                                            Q( name__icontains=query)
                     )
        query_args.append(kw_tag_qs)
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

    if kwargs:
        tag_qs = reduce(operator.and_, ( Q(**keyvalue)  for keyvalue in kwargs ))
        query_args.append(tag_qs)

    if query_args:
        query_final = reduce(operator.or_, (item for item in query_args))
        providers = Provider.objects.filter(query_final).distinct()

    if not query_args:
        providers = Provider.objects.all()

    paginator = Paginator(providers, number_per_page)

    page = request.GET.get('page', 1)
    try:
        providers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        providers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        providers = paginator.page(paginator.num_pages)

    results = []
    for provider in providers.object_list:
        results.append(provider.to_json())

    final_results = [ { 'providers' : results, 'has_next' : providers.has_next(),
                        'has_previous' : providers.has_previous(),
                        'count' : paginator.count,
                        'next_page_number' : providers.next_page_number(),
                        'previous_page_number' : providers.previous_page_number()} ]

    return HttpResponse(dumps(final_results),
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



