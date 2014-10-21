from django.db import models
from django.conf import settings

from .managers import EtfarManager

class Etfar(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.TextField(help_text='Start here, what is the event that transpired?')
    thought = models.TextField(blank=True, 
                               help_text='Thought about that Event')
    feeling = models.TextField(blank=True, 
                               help_text='Feelings from the Thought')
    action = models.TextField(blank=True, 
                              help_text='Actions I take when I have these Feelings')
    result = models.TextField(blank=True, 
                              help_text='Results I created from those Actions')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{}: {}'.format(self.owner.username, self.event)


class EtfarAccessCondition(models.Model):
    '''
    a condition that must be met to access etfar tool.
    a user object will be tested in manager. All conditions must be met to 
    access the etfar tool.
    '''
    package = models.ForeignKey("packages.Package")
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = EtfarManager()

    def __unicode__(self):
        return u"{}".format(self.package.name)
