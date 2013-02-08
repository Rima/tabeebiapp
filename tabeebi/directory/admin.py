from django.contrib import admin
from tabeebi.directory.models import *

admin.site.register(Network)
admin.site.register(NetworkCategory)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Area)

class DataStatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'enable')

admin.site.register(DataState, DataStatesAdmin)

class ProviderAdmin(admin.ModelAdmin):
    readonly_fields = ('location',)

#admin.site.register(Provider, ProviderAdmin)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('address1', 'address2')
#admin.site.register(Location, LocationAdmin)


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
admin.site.register(FrequentlyAskedQuestion, FAQAdmin)


class FlatTableAdmin(admin.ModelAdmin):
    list_display = ('provider', 'type', 'network', 'country', 'city', 'pobox', 'telephone', 'fax', 'location1', 'location2')

#admin.site.register(FlatTable, FlatTableAdmin)


class ProviderFullDetailsAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'city', 'area')
    search_fields = ('provider_name',)
    list_filter = ('provider_type', 'city', 'country')

admin.site.register( ProviderFullDetails, ProviderFullDetailsAdmin )