from django.conf.urls.defaults import *

urlpatterns = patterns('congress.views',
    
    url(r'^$', 
        'filter_legislators', 
        name="congress_legislators_all"),

    url(r'^(?P<member_id>\w{7})/$',
        'legislator_detail',
        name="congress_legislator_detail"),
    
    url(r'^(?P<state>[A-Za-z]{2})/$', 
        'filter_legislators', 
        name="congress_legislators_state"),
    
    url(r'^(?P<office>\w+)/$', 
        'filter_legislators', 
        name="congress_legislators_office"),
    
    url(r'^(?P<office>\w+)/(?P<state>[A-Za-z]{2})/$', 
        'filter_legislators',
        name="congress_legislators_office_state"),
)