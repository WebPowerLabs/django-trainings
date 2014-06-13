import json, re, requests

from django.shortcuts import get_object_or_404
from django.db import models
from django.db.models import permalink
from django.conf import settings

from jsonfield import JSONField

from .managers import FBGroupManager, FBPostManager


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
    pinned_comment = models.OneToOneField('django_comments.Comment', blank=True, null=True)

    objects = FBGroupManager()

    def __unicode__(self):
        return self.name if self.name else self.fb_uid

    @permalink
    def get_absolute_url(self):
        return 'facebook_groups:detail', (), {'fb_uid': self.fb_uid}

    def get_fb_data_url(self, user):
        """ get data about this facebook group
        """

        # get the fb token from requesting user
        fb_token = user.get_fb_access_token()
        if self.fb_uid:
            return "https://graph.facebook.com/v2.0/{}?access_token={}".format(self.fb_uid, fb_token.token)

    def get_fb_feed_url(self, user):
        """ get feed for this facebook group
        """

        # get the fb token from requesting user
        fb_token = user.get_fb_access_token()
        if self.fb_uid:
            return "https://graph.facebook.com/v2.0/{}/feed?limit=50&access_token={}".format(self.fb_uid, fb_token.token)

    def save_fb_profile_data(self, user):

        # get data from facebook to save
        fb_data = requests.get(self.get_fb_data_url(user))
        print fb_data
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
        from django_comments.models import Comment
        pin = get_object_or_404(Comment, id=comment_id)
        self.pinned_comment = pin
        self.save()
        return pin

    def unpin_comment(self):
        self.pinned_comment = None
        self.save()

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

