# -*- coding: utf-8 -*-
import requests

from django.db import models

from allauth.socialaccount.models import SocialApp
from users.models import User


class FBGroupManager(models.Manager):

	def fb_create(self, **kwargs):
		""" Creates a facebook group for the Facebook App
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

		post_url = "https://graph.facebook.com/v2.0/{0}/groups?admin={1}&name={2}&description={3}&privacy={4}&access_token={5}".format(
			client_id, fb_uid, name, description, privacy, access_token)
		print post_url
		new_group = requests.post(post_url)
		if new_group.ok:
			if not user:
				user = User.objects.filter(is_superuser=True)[0]
			new_group = self.create(fb_uid=new_group.json()["id"], owner=user)
		return new_group