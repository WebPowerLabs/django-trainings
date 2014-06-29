from django.db import models
from django.db.models import Q
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.core import urlresolvers
from django.template.loader import select_template

from .managers import FeatureManager

class Feature(models.Model):
    '''
    Through model for featuring items in a comment
    '''
    #CHOICES = ContentType.objects.filter(Q(name=u'lesson') | Q(name=u'course'))
    comment = models.ForeignKey('django_comments.Comment', related_name='features')
    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = FeatureManager()

    def __unicode__(self):
        return u'{} {}'.format(self.content_type.name, self.created)

    def get_content_object_url(self):
        """
        Get a URL suitable for redirecting to the content object.
        """
        return urlresolvers.reverse(
            "comments-url-redirect",
            args=(self.content_type_id, self.object_pk)
        )

    def get_template_url(self):
        """
        Get url to content_type's display
        """
        default_template = "features/feature_object.html"
        object_template = "features/feature_{}.html".format(self.content_type.name)
        return select_template([object_template, default_template])