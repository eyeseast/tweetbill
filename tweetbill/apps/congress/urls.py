from django.conf.urls.defaults import *

urlpatterns = patterns('congress.views',
    url(r'^search/$', 'search', name='congress_search'),
    
    # legislators
    url(r'^legislators/$', 
        'filter_legislators', 
        name="congress_legislators_all"),
    
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