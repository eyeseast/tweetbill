import datetime
from django.conf import settings

from congress.models import Committee, Legislator

from sunlight import Sunlight
from nytcongress import NytCongress, get_congress

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY'))
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY'))

def committees(*chambers):
    """
    Load committees from Sunlight
    """
    congress = get_congress(datetime.datetime.now().year)
    for chamber in chambers:
        committees = nyt.committees.filter(chamber.lower(), congress)
        
        for c in committees['committees']:
            try:
                committee = Committee.objects.get(id=c['id'])
            except Committee.DoesNotExist:
                committee = Committee(
                    id = c['id'],
                    chamber = chamber.lower(),
                    name = c['name']
                )
            
            # make sure we're still in the current congress
            committee.congress = congress
            committee.save()

def members(**kwargs):
    """
    Load members of Congress from Sunlight
    """
    legislators = sunlight.legislators.getList(**kwargs)
    for m in legislators:
        try:
            member = Legislator.objects.get(id=m['bioguide_id'])
        except Legislator.DoesNotExist:
            member = Legislator(
                id = m['bioguide_id'],
                title = m['title'],
                
                first_name = m['firstname'],
                middle_name = m['middlename'],
                last_name = m['lastname'],
                name_suffix = m['name_suffix'],
            )
            
            # other fields are just copied from Sunlight
            for k, v in m.items():
                if hasattr(member, k):
                    setattr(member, k, v)
            
            member.save()