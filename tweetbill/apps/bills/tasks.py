import datetime
import sys

from dateutil.parser import parse
from django.conf import settings

from tweetbill.lib.utils import parse_date

from bills.models import Bill, BillAction
from congress.models import Legislator, Committee

from nytcongress import NytCongress, get_congress
from sunlight import Sunlight

# Don't cache responses, so we always get the freshest info
nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None), None)
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None), cache=None)


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


def load_bills(verbose=False):
    """
    Load all recent bills
    """
    bills = get_recent_bills()
    for bill in bills:
        process_bill(bill)


def process_bill(bill_uri):
    """
    Load a bill into the database, sending out alerts for new actions.
        
    For each bill:
    - get the complete JSON representation, creating or updating an entry in the database
    - loop through actions, adding new ones to the database (see below on how to make actions unique)
    - fetch and add/update bill subjects
    - fetch and add/update bill cosponsors
    """
    try:
        nyt_bill = nyt.fetch(bill_uri)
    except ValueError:
        # sometimes there's bad JSON
        # this should be logged
        print '\nBill %s failed to load' % bill_uri
        return
    
    bill_id = nyt_bill['bill'].replace('.', '').lower()
    try:
        bill = Bill.objects.get(congress=int(nyt_bill['congress']), number=bill_id)
    except Bill.DoesNotExist:
        sponsor = Legislator.objects.get(nyt_uri__iexact=nyt_bill['sponsor_uri'])
        bill = Bill.objects.create(
            congress=int(nyt_bill['congress']), 
            number=bill_id,
            nyt_uri = bill_uri,
            title = nyt_bill['title'],
            introduced_date = parse_date(nyt_bill['introduced_date']),
            sponsor = sponsor,
        )
    
    print bill_uri
    set_bill_actions(bill, nyt_bill['actions'])

def set_bill_actions(bill, actions):
    """
    Given a bill and a list of actions (dict)
    add new ones to the bill
    """
    NEW_ACTIONS = []
    
    # make a copy before we do anything else
    # reverse orders so oldest actions are first
    actions = reversed(list(actions))
    
    # set datetimes to datetime objects
    # then check for existence in the db
    for i, action in enumerate(actions):
        action['datetime'] = parse_date(action['datetime'])
        action['id'] = u"%s-%s" % (bill.id, i)
        action['bill'] = bill
        action['index'] = i
        
        a, created = BillAction.objects.get_or_create(**action)
        if created:
            NEW_ACTIONS.append(a)
    
    #if NEW_ACTIONS:
    #    send_alerts(*NEW_ACTIONS)
    
def send_alerts(*actions):
    """
    Blast out alerts to anyone watching
    """
    # for now, just print out new actions
    print '\n'.join(actions)