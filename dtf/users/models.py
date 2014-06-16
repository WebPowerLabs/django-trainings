# -*- coding: utf-8 -*-
import hashlib
# Import the AbstractUser model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from allauth.socialaccount.models import SocialAccount


# Subclass AbstractUser
class User(AbstractUser):

    infusionsoft_uid = models.IntegerField(null=True, blank=True, unique=True)

    def __unicode__(self):
        return self.username

    def get_fb_profile_img_url(self):
    	fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
        if len(fb_uid):
            return "https://graph.facebook.com/v2.0/{}/picture?width=40&height=40".format(fb_uid[0].uid)

    def fb_photos(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')

        if len(fb_uid):
            return "https://graph.facebook.com/v2.0/{}/?fields=albums".format(fb_uid[0].uid)

    def get_fb_access_token(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')
        if fb_uid:
            return fb_uid[0].socialtoken_set.all()[0]

    def get_fb_extra_data(self):
        u_social = self.socialaccount_set.all()
        if u_social:
            return u_social[0].extra_data

    @property
    def fb_uid(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.id, provider='facebook')

        if len(fb_uid):
            return fb_uid[0].uid
        else:
            return None

'''
# signal dependencies
from django.db.models.signals import post_save
from django.dispatch import receiver

import djnfusion

@receiver(post_save, sender=User)
def djnfusion_sync_user(sender, **kwargs):
    user = kwargs['instance']
    djnfusion.sync_user(user)
'''    

