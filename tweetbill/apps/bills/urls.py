from django.conf.urls.defaults import *

urlpatterns = patterns('bills.views',
    url(r'start/$', 
        'public_timeline', 
        name='public_timeline'),
)