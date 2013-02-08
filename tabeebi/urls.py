from django.conf.urls import patterns, include, url
from django.conf  import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'tabeebi.views.home', name='home'),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
    url(r'^webservices/query/', 'tabeebi.directory.views.serializer'),

    url( r'^GetDataStates', 'tabeebi.directory.views.data_states'  ),
    url( r'^GetCountries', 'tabeebi.directory.views.countries_cities_list'  ),
    url( r'^GetInsuranceCompanies', 'tabeebi.directory.views.insurance_companies'  ),
    url( r'^GetPorviders', 'tabeebi.directory.views.providers_list'  ),
    url( r'^GetProviderTypes', 'tabeebi.directory.views.provider_types_list'  ),
    url( r'^GetFAQ', 'tabeebi.directory.views.faq'  ),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.ADMIN_STATIC}),


    #url( r'^refresh_data', 'tabeebi.directory.views.store_data_in_places'  ),
    url( r'^refresh_area_data', 'tabeebi.directory.views.extract_location_tags'  ),
    #url( r'^refresh_category_data', 'tabeebi.directory.views.store_countries_networks_cities'  ),

)
