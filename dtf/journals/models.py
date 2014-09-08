import datetime

from django.db import models
from django_hstore import hstore
from django.conf import settings

from positions import PositionField

from .managers import JournalQuestionManager


class JournalEntry(models.Model):
    journal = models.ForeignKey("journals.Journal")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    active = models.BooleanField(default=True)
    data = hstore.DictionaryField()

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u'{} {}'.format(self.journal.author.username, self.created)


class Journal(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL)

    @property
    def can_submit(self):
        '''
        returns true if an author can submit a journal entry now
        '''
        can_sumbit = True if not self._user_submitted_entry_today() else False
        return can_sumbit

    def _user_submitted_entry_today(self):
        '''
        Returns true if a journal entry was submitted today
        '''
        yesterday = datetime.datetime.now() - datetime.timedelta(1)
        entry_today = JournalEntry.objects.filter(journal=self, active=True, 
                                            created__gte=yesterday).exists()
        return entry_today


    def __unicode__(self):
        return u"{}".format(self.author.first_name)


class JournalQuestion(models.Model):
    FIELD_TYPES = (
                   ('char', 'Single-line Text'),
                   ('text', 'Multi-line Text'),)
    name = models.CharField(max_length=255)
    type = models.CharField(choices=FIELD_TYPES, default='char', max_length=4)
    active = models.BooleanField(default=True)
    position = PositionField()

    objects = JournalQuestionManager()

    @property
    def template_name(self):
        return self._get_template_name()

    def _get_template_name(self):
        return "journals/_{}_field.html".format(self.type)

    def __unicode__(self):
        return u"{}".format(self.name)
