from django.db import models

from django.conf import settings


class Etfar(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    event = models.TextField(help_text='Start here, what is the event that \
                             transpired?')
    thought = models.TextField(blank=True, 
                               help_text='Thought about that Event')
    feeling = models.TextField(blank=True, 
                               help_text='Feelings from the Thought')
    action = models.TextField(blank=True, 
                              help_text='Actions I take when I have these \
                              Feelings')
    result = models.TextField(blank=True, 
                              help_text='Results I created from those Actions')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{}: {}'.format(self.owner.username, self.event)