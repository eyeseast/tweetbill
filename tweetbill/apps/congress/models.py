import datetime
from django.conf import settings
from django.db import models

from nytcongress import NytCongress, get_congress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY'))
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY'))

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
        'first_name',
        'middle_name',
        'last_name',
        'name_suffix',
    )
    
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=5, blank=True)
    party = models.CharField(max_length=1, choices=PARTY_CHOICES)

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    name_suffix = models.CharField(max_length=10, blank=True, null=True)
    
    # ids for other services
    eventful_id = models.CharField(max_length=30, blank=True, null=True)
    crp_id = models.CharField(max_length=30, blank=True, null=True)
    fec_id = models.CharField(max_length=30, blank=True, null=True)
    govtrack_id = models.CharField(max_length=30, blank=True, null=True)
    twitter_id = models.CharField(max_length=100, blank=True, null=True)
    votesmart_id = models.CharField(max_length=30, blank=True, null=True)
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    def __unicode__(self):
        return u"%s (%s)" % (self.full_name, self.party)
    
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
    