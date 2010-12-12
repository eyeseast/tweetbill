import datetime
from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

from tweetbill.lib.managers import manager_from
from congress.models import Legislator, Committee

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
    "A bill. Only a bill."
    id = models.CharField(max_length=30, primary_key=True)
    congress = models.PositiveIntegerField()
    number = models.CharField(max_length=20)
    nyt_uri = models.URLField(verify_exists=False)
    title = models.CharField(max_length=255)
    introduced_date = models.DateField()
    latest_major_action_date = models.DateField(blank=True, null=True)
    
    sponsor = models.ForeignKey(Legislator, related_name="bills_sponsored")
    cosponsors = models.ManyToManyField(Legislator, related_name="bills_cosponsored", blank=True, null=True)
    committees = models.ManyToManyField(Committee, related_name="bills", blank=True, null=True)
    subjects = models.ManyToManyField(BillSubject, related_name="bills", blank=True, null=True)
    watchers = models.ManyToManyField(User, related_name="bills_watched", blank=True, null=True)
    
    class Meta:
        get_latest_by = "latest_major_action"
        ordering = ('-latest_major_action_date',)
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self._get_id()
        super(Bill, self).save(*args, **kwargs)
    
    def _get_id(self):
        "Get unique ID for a bill using Congress and bill number"
        return u"%s-%s" % (self.congress, self.number)


class BillAction(models.Model):
    """
    Something that happens in the life of a bill,
    as recorded on the last_major_action key in 
    NYT Congress API responses
    
    IDs are <congress>-<bill-number>-<index>
    """
    id = models.CharField(max_length=30, primary_key=True)
    bill = models.ForeignKey(Bill, related_name="actions")
    index = models.IntegerField()
    datetime = models.DateTimeField()
    description = models.TextField()
    
    # whose news feeds does this action go in
    watchers = models.ManyToManyField(User, related_name="bill_actions")
    
    class Meta:
        get_latest_by = "index"
        ordering = ('-index',)
    
    def __unicode__(self):
        return self.description
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = u"%s-%s" % (self.bill.id, self.index)
        super(BillAction, self).save(*args, **kwargs)
