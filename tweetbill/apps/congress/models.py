import datetime
import os

from django.conf import settings
from django.core.cache import cache
from django.contrib.localflavor.us.models import USStateField, PhoneNumberField
from django.db import models

from nytcongress import NytCongress, get_congress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY'), cache)
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY'), cache=cache)

class Committee(models.Model):
    """
    A House, Senate or Joint committee
    """
    CHAMBER_CHOICES = (
        ('house', 'House'),
        ('senate', 'Senate'),
        ('joint', 'Joint')
    )
    
    id = models.CharField(max_length=5, primary_key=True)
    chamber = models.CharField(max_length=10, choices=CHAMBER_CHOICES)
    congress = models.IntegerField()
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ('-congress', 'chamber', 'name')
    
    def __unicode__(self):
        return self.name
    
    def save(self):
        if not self.congress:
            self.congress = get_congress(datetime.datetime.now().year)
        super(Committee, self).save()
    
    @property
    def members(self):
        if not hasattr(self, '_members'):
            self._members = sunlight.committees.get(id=self.id).get('members')
        return self._members

class Legislator(models.Model):
    """
    A member of Congress, in either the Senate or House.
    We're storing as little info here as we can and relying
    on the NYT and Sunlight APIs for details.
    """
    CHAMBER_CHOICES = (
        ('house', 'House of Representatives'),
        ('senate', 'Senate'),
    )
    
    PARTY_CHOICES = (
        ('D', 'Democrat'),
        ('R', 'Republican'),
        ('I', 'Independent'),
    )
    
    NAME_FIELDS = (
        'firstname',
        'middlename',
        'lastname',
        'name_suffix',
    )
    
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=5, blank=True)
    party = models.CharField(max_length=1, choices=PARTY_CHOICES)
    nyt_uri = models.URLField(max_length=255, verify_exists=False)    
    state = USStateField()

    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    name_suffix = models.CharField(max_length=10, blank=True, null=True)
    
    # ids for other services
    eventful_id = models.CharField(max_length=30, blank=True, null=True)
    crp_id = models.CharField(max_length=30, blank=True, null=True)
    fec_id = models.CharField(max_length=30, blank=True, null=True)
    govtrack_id = models.CharField(max_length=30, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)
    votesmart_id = models.CharField(max_length=30, blank=True, null=True)
    
    # contact info
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    
    class Meta:
        ordering = ('lastname', 'firstname')
    
    def __unicode__(self):
        return u"%s. %s (%s-%s)" % (self.title, self.full_name, self.party, self.state)
    
    def save(self, *args, **kwargs):
        if not self.nyt_uri:
            self.nyt_uri = "http://api.nytimes.com/svc/politics/v3/us/legislative/congress/members/%s.json" \
                % self.id
        super(Legislator, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        return ("congress_legislator_detail", None, {'member_id': self.id})
    
    @property
    def full_name(self):
        parts = filter(bool, [getattr(self, f) for f in self.NAME_FIELDS])
        return ' '.join(parts)
    
    @property
    def common_name(self):
        parts = filter(bool, [getattr(self, f) for f in self.NAME_FIELDS])
        if self.nickname:
            parts[0] = self.nickname
        return ' '.join(parts)
    
    def image(self, size='large'):
        return os.path.join(
            settings.MEDIA_URL,
            'img', 'legislators',
            size, '%s.jpg' % self.id
        )