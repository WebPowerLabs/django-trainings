import json, re, requests

from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import permalink
from django.conf import settings

from allauth.socialaccount.models import SocialApp

from jsonfield import JSONField
from dtf_comments.models import DTFComment

from .managers import FBGroupManager, FBPostManager
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.db.models import Q
from utils.search import EsClient
from django.contrib.auth import get_user_model



class FacebookGroup(models.Model):
    fb_uid = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    venue = models.TextField(blank=True)
    privacy = models.CharField(max_length=255, blank=True)
    icon = models.URLField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    feed = models.TextField(blank=True)
    pinned_post = models.OneToOneField('FacebookPost', blank=True, null=True)
    pinned_comment = models.OneToOneField('dtf_comments.DTFComment',
                                          blank=True, null=True)
    thumbnail = models.ImageField(upload_to='fb_groups/thumbs/%Y/%m/%d',
                height_field='thumbnail_height', width_field='thumbnail_width',
                blank=True, null=True)
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    cover = models.ImageField(upload_to='fb_groups/covers/%Y/%m/%d',
                height_field='cover_height', width_field='cover_width',
                blank=True, null=True)
    cover_height = models.CharField(max_length=255, blank=True)
    cover_width = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    objects = FBGroupManager()

    def __unicode__(self):
        return self.name if self.name else self.fb_uid

    @property
    def social_app(self):
        return SocialApp.objects.all()[0]

    @property
    def client_id(self):
        return self.social_app.client_id

    @permalink
    def get_absolute_url(self):
        return 'facebook_groups:detail', (), {'fb_uid': self.fb_uid}

    def get_fb_data_url(self, user):
        """ get data about this facebook group
        """
        if self.fb_uid:
            return "https://graph.facebook.com/v2.0/{}?access_token={}|{}".format(
                self.fb_uid, self.social_app.client_id, self.social_app.secret)

    def get_fb_feed_url(self, user):
        """ get feed for this facebook group
        """
        if self.fb_uid:
            return "https://graph.facebook.com/v2.0/{}/feed?limit=50&access_token={}|{}".format(
                self.fb_uid, self.social_app.client_id, self.social_app.secret)

    def save_fb_profile_data(self, user):

        # get data from facebook to save
        fb_data = requests.get(self.get_fb_data_url(user))
        if fb_data:
            fb_data_json = fb_data.json()
            self.name = fb_data_json["name"]
            self.description = fb_data_json["description"]
            self.venue = fb_data_json["venue"]
            self.privacy = fb_data_json["privacy"]
            self.icon = fb_data_json["icon"]
            self.email = fb_data_json["email"]
            self.save()

    def get_fb_feed(self, user):

        # get data from facebook to save
        fb_feed = requests.get(self.get_fb_feed_url(user))
        if fb_feed:
            return fb_feed.json()

    def post_fb_feed(self, user, message):
        """
        post new comment to this groups feed
        """
        post_url = "%s&message=%s" % (self.get_fb_feed_url(user), message)
        post = requests.post(post_url)
        return post

    def pin_post(self, user, post_fb_uid):
        try:
            pin = FacebookPost.objects.get(fb_uid=post_fb_uid)
        except FacebookPost.DoesNotExist:
            pin = FacebookPost.objects.fb_create(user=user, fb_uid=post_fb_uid)
        self.pinned_post = pin
        self.save()
        return pin

    def pin_comment(self, comment_id):
        pin = get_object_or_404(DTFComment, id=comment_id)
        self.pinned_comment = pin
        self.save()
        return pin

    def unpin_comment(self):
        self.pinned_comment = None
        self.save()

    def get_members(self):
        User = get_user_model()
        if self.package_set.count():
            return User.objects.filter(is_active=True
                     ).filter(Q(packagepurchase__package__groups=self,
                                packagepurchase__status=1)).distinct()
        else:
            return User.objects.filter(is_active=True)


class FacebookPost(models.Model):
    fb_uid = models.CharField(max_length=255, unique=True)
    from_user = JSONField(blank=True)
    to_user = JSONField(blank=True)
    message = models.TextField(blank=True)
    actions = models.TextField(blank=True)
    privacy = models.TextField(blank=True)
    created_time = models.TextField(blank=True)
    updated_time = models.TextField(blank=True)

    objects = FBPostManager()

    def __unicode__(self):
        return u'%s' % self.fb_uid


@receiver(post_save, sender=FacebookGroup)
def index_es_doc(instance, **kwarg):
    EsClient(instance).index()


@receiver(post_delete, sender=FacebookGroup)
def delete_es_doc(instance, **kwarg):
    EsClient(instance).delete()

