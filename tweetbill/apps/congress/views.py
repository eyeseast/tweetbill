from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from sunlight import Sunlight
from nytcongress import NytCongress, get_congress

sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY'))
nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY'))

OFFICE_TITLES = {
    'house': 'Rep',
    'senate': 'Sen'
}

def search(request):
    """
    Search legislators by name using sunlight.legislators.search
    """
    name = request.GET.get('name')
    if name:
        results = sunlight.legislators.search(name=name)
    else:
        results = []
    
    return render_to_response('congress/search.html', {
                              'name': name, 'results': results
                              }, RequestContext(request))

def filter_legislators(request, **kwargs):
    template = kwargs.pop('template', 'congress/legislator_list.html')
    
    if 'office' in kwargs:
        kwargs['title'] = OFFICE_TITLES[kwargs.pop('office').lower()]
    
    legislators = sunlight.legislators.getList(**kwargs)
    legislators = (l['legislator'] for l in legislators)
    
    return render_to_response(template, {'legislators': legislators}, RequestContext(request))