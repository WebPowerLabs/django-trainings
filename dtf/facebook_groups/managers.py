# -*- coding: utf-8 -*-
import requests

from django.db import models

from django.db.models import Q
from allauth.socialaccount.models import SocialApp
from users.models import User


class FBGroupManager(models.Manager):
    def purchased(self, user):
        if user.is_authenticated():
            if user.is_staff:
                return self.all()
        return self.filter(Q(package__packagepurchase__user=user,
                           package__packagepurchase__status=1) |
                           Q(package=None))

    def fb_create(self, **kwargs):
        """ Creates a facebook group for the Facebook App
        arguments:
        name
        description
        privacy
        user
        """
        social_app = SocialApp.objects.all()[0]
        client_id = social_app.client_id
        # access_token = social_app.socialtoken_set.all()[0] # this token isn't working
        access_token = "{0}|{1}".format(client_id, social_app.secret)
        name = kwargs.get("name") if kwargs.get("name") else "%s Test Group" % social_app.get_provider_display()
        description = kwargs.get("description") if kwargs.get("description") else "%s Test Group" % social_app.get_provider_display()
        privacy = kwargs.get("privacy") if kwargs.get("privacy") else "closed"
        user = None

        if kwargs.get("user"):
            try:
                user = User.objects.get(id=kwargs.get("user"))
            except User.DoesNotExist:
                try:
                    user = User.objects.get(fb_uid=kwargs.get("user"))
                except User.DoesNotExist:
                    print "User with id or fb_uid %s Does Not Exist" % str(fb_uid=kwargs.get("user"))
                    raise
        # set the fb_uid to user if a user that exists was given and has a fb_uid else user Will's fb_uid
        fb_uid = user.fb_uid if user and user.fb_uid else u'100003511777674'

        post_url = "https://graph.facebook.com/v2.0/{0}/groups?&name={2}&description={3}&privacy={4}&access_token={5}".format(
            client_id, fb_uid, name, description, privacy, access_token)
        print post_url
        new_group = requests.post(post_url)
        if not user:
            user = User.objects.filter(is_superuser=True)[0]
        if new_group.ok:
            new_group = self.create(fb_uid=new_group.json()["id"], owner=user)
        else:
            new_group = self.create(owner=user)

        return new_group


class FBPostManager(models.Manager):

    def fb_create(self, **kwargs):
        """ Creates a facebook group for the Facebook App
        arguments:
        name
        description
        privacy
        user
        """
        social_app = SocialApp.objects.all()[0]
        client_id = social_app.client_id
        access_token = "{0}|{1}".format(client_id, social_app.secret)
        user = None
        fb_post = None

        if kwargs.get('fb_uid'):
            # if theres a fb_uid then were fetching an existing post
            fb_uid = kwargs.get('fb_uid')
            # create the beginning of the request url
            fb_get_url = "https://graph.facebook.com/v2.0/{0}".format(fb_uid)
            if kwargs.get("user"):
                # if there's a user argument then use the user's acces token instead of the apps
                user = kwargs.get('user')
                access_token = user.get_fb_access_token().token
            # format url with access token
            fb_get_url = "{0}?access_token={1}".format(fb_get_url, access_token)
            fb_post_request = requests.get(fb_get_url)
            print fb_post_request
            if fb_post_request.ok:
                # if request 200 create a new FB post object in database
                fb_post_json = fb_post_request.json()
                fb_post = self.create(
                    fb_uid=fb_post_json['id'],
                    from_user=fb_post_json['from'],
                    to_user=fb_post_json['to'],
                    message=fb_post_json['message'],
                    privacy=fb_post_json['privacy'],
                    actions=fb_post_json['actions'],
                    created_time=fb_post_json['created_time'],
                    updated_time=fb_post_json['updated_time'],
                    )
            else: fb_post = fb_post_request
        return fb_post
