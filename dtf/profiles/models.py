from django.db import models
from django.conf import settings

from jsonfield import JSONField


class CourseProfile(models.Model):
    ''' 
    for storing information about courses
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    history = JSONField(default="{}")
    favorites = JSONField(default="{}")


class LessonProfile(models.Model):
    ''' 
    for storing information about Lessons
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    history = JSONField(default="{}")
    favorites = JSONField(default="{}")


#class PackageProfile(models.Model):
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