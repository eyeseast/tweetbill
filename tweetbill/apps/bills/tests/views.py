from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from bills.tasks import load_bills
from bills.views import nyt, sunlight

from congress import load

class ActionsTest(TestCase):
    
    def setUp(self):
        load.members()
        load_bills()
    
    def test_public_timeline(self):
        resp = self.client.get(reverse('public_timeline'))
        self.assertEqual(resp.status_code, 200)
        
        actions = BillAction.objects.all()[:20]
        self.assertEqual(
            list(actions),
            list(resp.context['actions'])
        )

class UserTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('bob', 'bob@example.com', 'password')
        