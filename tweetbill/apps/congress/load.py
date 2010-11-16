import datetime
from django.conf import settings

from congress.models import Committee

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
