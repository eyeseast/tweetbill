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