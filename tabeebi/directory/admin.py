from django.contrib import admin
from tabeebi.directory.models import *

admin.site.register(Network)
admin.site.register(NetworkCategory)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(City)

class DataStatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'enable')

admin.site.register(DataState, DataStatesAdmin)

class ProviderAdmin(admin.ModelAdmin):
    readonly_fields = ('location',)

admin.site.register(Provider, ProviderAdmin)

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
admin.site.register(FrequentlyAskedQuestion, FAQAdmin)


class FlatTableAdmin(admin.ModelAdmin):
    list_display = ('provider', 'type', 'network', 'country', 'city', 'pobox', 'telephone', 'fax', 'location1', 'location2')

admin.site.register(FlatTable, FlatTableAdmin)