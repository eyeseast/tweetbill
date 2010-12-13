import random
from django.conf import settings
from django.test import TestCase

from bills.models import Bill, BillAction
from bills.tasks import get_recent_bills, process_bill, load_bills, parse_date

from congress import load

from nytcongress import NytCongress, get_congress
from sunlight import Sunlight

# Don't cache responses, so we always get the freshest info
nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None), None)
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None), cache=None)


class LoaderTest(TestCase):
    
    def setUp(self):
        load.members()
        load_bills()
    
    def test_bill_count(self):
        recent = get_recent_bills()
        self.assertEqual(len(recent), Bill.objects.count())
    
    def test_bills_loaded(self):
        failed = []
        for bill_uri in get_recent_bills():
            try:
                Bill.objects.get(nyt_uri__iexact=bill_uri)
            except Bill.DoesNotExist:
                failed.append(bill_uri)
        
        if failed:
            self.fail('\n'.join(failed))
    
    def test_double_load(self):
        # bills are loaded in setUp, so load again
        recent = get_recent_bills()
        load_bills()
        self.assertEqual(len(recent), Bill.objects.count())

class BillTest(TestCase):
    
    def setUp(self):
        load.members()
        self.recent_bills = get_recent_bills()
    
    def test_bill_actions(self):
        bill_info = nyt.bills.get('hr1', 111) # the stimulus
        process_bill(bill_info['bill_uri'])
        bill = Bill.objects.get(congress=111, number='hr1')
        
        self.assertEqual(
            len(bill_info['actions']),
            bill.actions.count()
        )
        
        for a1, a2 in zip(bill_info['actions'], bill.actions.all()):
            self.assertEqual(a1['description'], a2.description)
            self.assertEqual(
                parse_date(a1['datetime']),
                a2.datetime
            )
        
    
    def test_bill_details(self):
        bill_uri = random.choice(list(self.recent_bills))
        bill_info = nyt.fetch(bill_uri)
        process_bill(bill_uri)
        bill = Bill.objects.get(nyt_uri=bill_uri)
        
        self.assertEqual(
            bill_info['sponsor_uri'],
            bill.sponsor.nyt_uri
        )
        
        self.assertEqual(
            bill_info['title'],
            bill.title
        )
        
        self.assertEqual(
            bill.nyt_uri,
            bill_uri,
        )