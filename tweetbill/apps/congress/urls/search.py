from django.conf.urls.defaults import *

urlpatterns = patterns('congress.views',
    
    # search
    url(r'^$', 'search', name='congress_search'),
    
    url(r'^zip/$', 'legislators_for_zip'),
    
    url(r'^zip/(?P<zipcode>\d{5})/$',
        'legislators_for_zip',
        name="congress_search_zip"),
)