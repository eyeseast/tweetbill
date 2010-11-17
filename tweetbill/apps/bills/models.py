import datetime
from django.conf import settings
from django.db import models

from tweetbill.lib.managers import manager_from

from nytcongress import NytCongress, get_congress
from sunlight import Sunlight

nyt = NytCongress(getattr(settings, 'NYT_CONGRESS_API_KEY', None))
sunlight = Sunlight(getattr(settings, 'SUNLIGHT_API_KEY', None))


class BillSubject(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name


class Bill(models.Model):
    pass


class BillAction(models.Model):
    """
    Something that happens in the life of a bill,
    as recorded on the last_major_action key in 
    NYT Congress API responses
    """
    bill = models.ForeignKey(Bill, related_name="actions")
    datetime = models.DateTimeField()
    description = models.TextField()
    
    class Meta:
        get_latest_by = "datetime"
        ordering = ('-datetime',)
    
    def __unicode__(self):
        return self.description