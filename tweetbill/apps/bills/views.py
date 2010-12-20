from django.conf import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from nytcongress import NytCongress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None), cache)
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None), cache=cache)

def public_timeline(request):
    """
    Recent bill actions for all bills
    
    :actions::
        20 latest bill actions
    """
    actions = BillAction.objects.all()[:20]
    return render_to_response('bills/public_timeline.html',
        {'actions': actions},
        RequestContext(request))