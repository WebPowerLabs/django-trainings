from django.db import models
from django.conf import settings

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


class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.user.username
