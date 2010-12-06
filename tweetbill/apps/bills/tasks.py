from django.conf import settings

from bills.models import Bill, BillAction
from congress.models import Legislator, Committee

from nytcongress import NytCongress, get_congress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None))
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None))

def get_recent_bills():
    """
    Get four sets of recent bills--introduced and updated for House and Senate--
    and return a combined set, so that we only load each bill once.
    """
    
    hi = set(b['bill_uri'] for b in nyt.bills.introduced('house')['bills'])
    si = set(b['bill_uri'] for b in nyt.bills.introduced('senate')['bills'])
    
    hu = set(b['bill_uri'] for b in nyt.bills.updated('house')['bills'])
    su = set(b['bill_uri'] for b in nyt.bills.introduced('senate')['bills'])
    
    return hi | si | hu | su

def process_bill(bill_uri):
    """
    Load a bill into the database, sending out alerts for new actions.
        
    For each bill:
    - get the complete JSON representation, creating or updating an entry in the database
    - loop through actions, adding new ones to the database (see below on how to make actions unique)
    - fetch and add/update bill subjects
    - fetch and add/update bill cosponsors
    """
    nyt_bill = nyt.fetch(bill_uri)
    bill_id = nyt_bill['number'].replace('.', '').lower()
    try:
        bill = Bill.objects.get(congress=int(nyt_bill['congress']), number=bill_id)