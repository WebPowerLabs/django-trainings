from django.db import models
from django_hstore import hstore
from django.conf import settings



class JournalEntry(models.Model):
    journal = models.ForeignKey("journals.Journal")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    active = models.BooleanField(default=True)
    data = hstore.DictionaryField()

    class Meta:
        ordering = ('-created',)
        get_latest_by = ('-created',)

    def __unicode__(self):
        return u'{} {}'.format(self.journal.author.username, self.created)

class Journal(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return u"{}".format(self.author.first_name)


class JournalQuestion(models.Model):
    FIELD_TYPES = (
                   ('char', 'Single-line Text'),
                   ('text', 'Multi-line Text'),)
    name = models.CharField(max_length=20)
    type = models.CharField(choices=FIELD_TYPES, default='char', max_length=4)
    active = models.BooleanField(default=True)

    @property
    def template_name(self):
        return self._get_template_name()

    def _get_template_name(self):
        return "journals/_{}_field.html".format(self.type)

    def __unicode__(self):
        return u"{}".format(self.name)
