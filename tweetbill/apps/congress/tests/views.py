from django.conf import settings
from django.test import TestCase

from congress import load
from congress.models import Committee, Legislator

from nytcongress import NytCongress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None))
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None))

class ViewTest(TestCase):
    
    def test_search(self):
        resp = self.client.get('/search/', {'name': 'Nancy Pelosi'})
        results = sunlight.legislators.search(name='Nancy Pelosi')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['results'], results)

    def test_search_zip(self):
        resp = self.client.get('/search/zip/22206/')
        results = sunlight.legislators.allForZip(zip=22206)
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_house_list(self):
        resp = self.client.get('/legislators/house/')
        results = sunlight.legislators.getList(title='Rep')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_state_list(self):
        resp = self.client.get('/legislators/ca/')
        results = sunlight.legislators.getList(state='ca')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_office_state_list(self):
        resp = self.client.get('/legislators/senate/me/')
        results = sunlight.legislators.getList(state='me', title='Sen')
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_legislator_detail(self):
        load.members(title='Sen')
        resp = self.client.get('/legislators/S000320/') # Richard Shelby
        
        self.assertEqual(resp.status_code, 200)
        try:
            shelby = resp.context['member']
        except Exception, e:
            self.fail(e)
            return
        
        
        
        
    
class BadViewTest(TestCase):
    
    def test_bad_office(self):
        resp = self.client.get('/legislators/notachamber/')
        self.assertEqual(resp.status_code, 404)


