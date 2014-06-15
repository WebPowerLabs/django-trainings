from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import UUIDField
from django.db import models
from django.conf import settings


class History(models.Model):
    """
    for storing history for lessons and courses.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = UUIDField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['created']
        verbose_name_plural = 'History'


class Favourite(models.Model):
    """
    for storing favourites for lessons and courses.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType)
    object_id = UUIDField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['created']


# class PackageProfile(models.Model):
#    '''
#    for storing information about Packages
#    '''
#    user = models.OneToOneField(settings.AUTH_USER_MODEL)
#    packages = models.ManyToManyField("packages.Package")


class FacebookProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    fb_uid = models.TextField(blank=True)


class InfusionsoftProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    infusionsoft_uid = models.TextField(blank=True)
