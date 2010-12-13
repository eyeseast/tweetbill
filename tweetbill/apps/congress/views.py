from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from congress.models import Committee, Legislator

from nytcongress import NytCongress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None), cache)
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None), cache)

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

def legislator_detail(request, member_id):
    member = get_object_or_404(Legislator, id__iexact=member_id)
    bills = {
        'introduced': nyt.bills.by_member(member_id, 'introduced')['bills'],
        'updated'   : nyt.bills.by_member(member_id, 'updated')['bills']
    }
    return render_to_response('congress/legislator_detail.html', {
                              'member': member, 'bills': bills
                              }, RequestContext(request))

def legislators_for_zip(request, zipcode=None):
    if zipcode:
        legislators = sunlight.legislators.allForZip(zip=zipcode)
        return render_to_response('congress/legislator_list.html', {
                                  'legislators': legislators, 'zip': zipcode
                                  }, RequestContext(request))
    
    elif request.GET.get('zip'):
        return redirect(reverse(legislators_for_zip), zipcode)
    
    else: # no zipcode given
        return redirect(reverse(search))

def filter_legislators(request, **kwargs):
    template = kwargs.pop('template', 'congress/legislator_list.html')
    
    if 'office' in kwargs:
        try:
            kwargs['title'] = OFFICE_TITLES[kwargs.pop('office').lower()]
        except KeyError:
            raise Http404
    
    legislators = sunlight.legislators.getList(**kwargs)    
    return render_to_response(template, {'legislators': legislators}, RequestContext(request))