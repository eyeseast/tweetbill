from django.conf import settings
from django.test import TestCase

from sunlight import Sunlight
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY'))

class ViewTest(TestCase):
    
    def test_search(self):
        resp = self.client.get('/search/', {'name': 'Nancy Pelosi'})
        results = sunlight.legislators.search(name='Nancy Pelosi')
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['results'], results)

    def test_search_zip(self):
        resp = self.client.get('/search/zip/22206/')
        results = sunlight.legislators.allForZip(zip=22206)
        results = [r['legislator'] for r in results]
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_house_list(self):
        resp = self.client.get('/legislators/house/')
        results = sunlight.legislators.getList(title='Rep')
        results = [r['legislator'] for r in results]
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_state_list(self):
        resp = self.client.get('/legislators/ca/')
        results = sunlight.legislators.getList(state='ca')
        results = [r['legislator'] for r in results]
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context['legislators']), results)
    
    def test_office_state_list(self):
        resp = self.client.get('/legislators/senate/me/'),
        results = sunlight.legislators.getList(state='me', title='Sen')
    
