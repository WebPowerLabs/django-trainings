from django.db import models
from django_extensions.db.fields import AutoSlugField, UUIDField
from resources.managers import ResourceManager
from django.conf import settings


class Resource(models.Model):
    """ Resource
    A resource for a lesson. can include a file or just use description.
    Have several fields available incase resource wants its own detailview
    """
    objects = ResourceManager()

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
    thumbnail = models.FileField(upload_to='resources/thumbs/%Y/%m/%d',
                                                                    blank=True)
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    type = models.CharField(choices=TYPE_CHOICES, default='resource',
        max_length=255)
    lesson = models.ForeignKey('lessons.Lesson', null=255, blank=True)
    file = models.FileField(upload_to='resources/files/%Y/%m/%d', blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        order = None
        if not self.pk:
            order = self.lesson.get_resource_order()
        super(Resource, self).save(*args, **kwargs)
        if order:
            order.append(self.pk)
            self.lesson.set_resource_order(order)

    class Meta:
        ordering = ['_order', ]
        get_latest_by = '_order'
        order_with_respect_to = 'lesson'

    def __unicode__(self):
        return "{}[{}]".format(self.name, self.type)
