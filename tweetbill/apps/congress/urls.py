from django.conf.urls.defaults import *

urlpatterns = patterns('congress.views',
    url(r'^search/$', 'search', name='congress_search'),
)