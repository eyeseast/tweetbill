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