from django.db import models
from django_extensions.db.fields import AutoSlugField, UUIDField

import positions


class Resource(models.Model):
	""" Resource
	A resource for a lesson. can include a file or just use description.
	Have several fields available incase resource wants its own detailview
	"""

	TYPE_CHOICES = (
		('resource', 'Resource'),
		('homework', 'Homework'),
		)
	id = UUIDField(primary_key=True)
	name = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='name')
	description = models.TextField(blank=True, 
		help_text='a brief description of this resource')
	published = models.BooleanField(default=False, 
		help_text='users will only see published resources')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	order = positions.PositionField()
	thumbnail = models.FileField(upload_to='resources/thumbs/%Y/%m/%d', blank=True)
	thumbnail_height = models.CharField(max_length=255, blank=True)
	thumbnail_width = models.CharField(max_length=255, blank=True)
	type = models.CharField(choices=TYPE_CHOICES, default='resource', 
		max_length=255)
	lesson = models.ForeignKey('lessons.Lesson', null=255, blank=True)
	file = models.FileField(upload_to='resources/files/%Y/%m/%d', blank=True)


	class Meta:
		ordering = ['order',]
		order_with_respect_to = 'lesson'
		get_latest_by = 'order'