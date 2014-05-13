import json, re, requests

from django.db import models
from django.conf import settings


class FacebookGroup(models.Model):
	fb_uid = models.CharField(max_length=255)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL)
	name = models.CharField(max_length=255, blank=True)
	#description = models.TextField(blank=True)
	venue = models.TextField(blank=True)
	privacy = models.CharField(max_length=255, blank=True)
	icon = models.URLField(max_length=255, blank=True)
	email = models.EmailField(max_length=255)


	def get_fb_data_url(self, user):
		""" get data about this facebook group
		"""

		# get the fb token from requesting user
		fb_token = user.get_fb_access_token()
		if self.fb_uid:
			return "https://graph.facebook.com/v2.0/{}?access_token={}".format(self.fb_uid, fb_token)

	def get_fb_feed_url(self, user):
		""" get feed for this facebook group
		"""
		
		# get the fb token from requesting user
		fb_token = user.get_fb_access_token()
		if self.fb_uid:
			return "https://graph.facebook.com/v2.0/{}/feed?limit=50&access_token={}".format(self.fb_uid, fb_token)

	def save_fb_profile_data(self, user):

		# get data from facebook to save
		fb_data = requests.get(self.get_fb_data_url(user))
		print fb_data
		if fb_data:
			fb_data_json = fb_data.json()
			self.name = fb_data_json["name"]
			#self.description = fb_data_json["description"]
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
		post_url = "%s?message=%s" % (self.get_fb_feed_url(user), message)
		post = requests.post(post_url)
		return post

