from django.db import models
from django_extensions.db.fields import AutoSlugField


class Tag(models.Model):
	""" Tag
	Can be refrenced by other models with a M2M so that model is returned when
	filtering tags or search
	"""
	name = models.CharField(max_length=255)
	slug = AutoSlugField(populate_from='name')

	def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)

	def __unicode__(self):
		return self.name