from django.conf import settings
from django.test import TestCase

from congress import load
from congress.models import Committee, Legislator

from nytcongress import NytCongress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None))
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None))

class LoaderTest(TestCase):
    
    def test_load_committees(self):
        chambers = 'House', 'Senate', 'Joint'
        load.committees(*chambers)
        for chamber in chambers:
            # using sets here because ordering may be different
            comms = set(c['name'] for c in nyt.committees.filter(chamber.lower())['committees'])
            names = set(c.name for c in Committee.objects.filter(chamber=chamber.lower()))
            self.assertEqual(comms, names)
    
    def test_load_members(self):
        congress = sunlight.legislators.getList()
        load.members()
        members = Legislator.objects.all()
        self.assertEqual(
            set(m.id for m in members),
            set(c['bioguide_id'] for c in congress)
        )

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
                except Committee.DoesNotExist, e:
                    self.fail("%s does not exist" % bill['committees'])
            
            else: # it's a list
                for comm in bill['committees']:
                    c = Committee.objects.get(name=comm)
                    self.assertEqual(c.name, comm)
                