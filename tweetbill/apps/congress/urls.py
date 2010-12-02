from django.conf.urls.defaults import *

urlpatterns = patterns('congress.views',
    
    # search
    url(r'^search/$', 'search', name='congress_search'),
    
    url(r'^search/zip/$', 'legislators_for_zip'),
    
    url(r'^search/zip/(?P<zipcode>\d{5})/$',
        'legislators_for_zip',
        name="congress_search_zip"),
    
    # legislators
    url(r'^legislators/$', 
        'filter_legislators', 
        name="congress_legislators_all"),

    url(r'^legislators/(?P<member_id>\w{7})/$',
        'legislator_detail',
        name="congress_legislator_detail"),
    
    url(r'^legislators/(?P<state>[A-Za-z]{2})/$', 
        'filter_legislators', 
        name="congress_legislators_state"),
    
    url(r'^legislators/(?P<office>\w+)/$', 
        'filter_legislators', 
        name="congress_legislators_office"),
    
    url(r'^legislators/(?P<office>\w+)/(?P<state>[A-Za-z]{2})/$', 
        'filter_legislators',
        name="congress_legislators_office_state"),
)