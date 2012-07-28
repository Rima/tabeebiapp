from django.contrib import admin
from tabeebi.directory.models import Provider, Location, Network, NetworkCategory

admin.site.register(Network)
admin.site.register(NetworkCategory)
admin.site.register(Location)
admin.site.register(Provider)