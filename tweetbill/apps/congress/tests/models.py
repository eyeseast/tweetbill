from django.conf import settings
from django.test import TestCase

from congress import load
from congress.models import Committee

from nytcongress import NytCongress
nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY'))

class LoaderTest(TestCase):
    
    def test_load_committees(self):
        chambers = 'House', 'Senate', 'Joint'
        load.committees(*chambers)
        for chamber in chambers:
            # using sets here because ordering may be different
            comms = set(c['name'] for c in nyt.committees.filter(chamber.lower())['committees'])
            names = set(c.name for c in Committee.objects.filter(chamber=chamber.lower()))
            self.assertEqual(comms, names)
        

class CommitteeTest(TestCase):
    
    def setUp(self):
        load.committees('House', 'Senate', 'Joint')
        super(CommitteeTest, self).setUp()
    
    def test_bill_committees(self):
        bills = nyt.bills.introduced('house', 111)
        for bill in bills['bills']:
            
            if bill['committees'] and isinstance(bill['committees'], basestring):
                try:
                    comm = Committee.objects.get(name=bill['committees'])
                    self.assertEqual(comm.name, bill['committees'])
                except Committee.DoesNotExist:
                    print(bill['committees'])
                    self.fail()
            
            else: # it's a list
                for comm in bill['committees']:
                    c = Committee.objects.get(name=comm)
                    self.assertEqual(c.name, comm)
                