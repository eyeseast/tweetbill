import random

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from congress import load
from congress.models import Committee, Legislator
from congress.views import nyt, sunlight


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
        load.members()
        failed = []
        members = random.sample(sunlight.legislators.getList(), 10)
        for member in members:
            try:
                m = Legislator.objects.get(id=member['bioguide_id'])
                resp = self.client.get(reverse('congress_legislator_detail', args=(member['bioguide_id'],)))
                self.assertEqual(m.id, member['bioguide_id'])
                #self.assertEqual(
                #    nyt.bills.by_member(m.id)['bills'],
                #    resp.context['bills']['introduced']
                #)
            except Exception, e:
                failed.append(m.full_name + '\n' + str(e))
        
        if failed:
            self.fail('\n'.join(failed))
        
    
class BadViewTest(TestCase):
    
    def test_bad_office(self):
        resp = self.client.get('/legislators/notachamber/')
        self.assertEqual(resp.status_code, 404)


