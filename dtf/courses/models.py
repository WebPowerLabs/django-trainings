from django.db import models
from django_extensions.db.fields import AutoSlugField, UUIDField
from courses.managers import CourseManager


class Course(models.Model):
    """ Course
    Courses are a series of Lessons
    """
    objects = CourseManager()

    id = UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(blank=True,
        help_text='a brief summary of this course')
    published = models.BooleanField(default=False,
                            help_text='users will only see published courses')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.IntegerField(editable=False, default=0)
    thumbnail = models.ImageField(upload_to='courses/thumbs/%Y/%m/%d',
                height_field='thumbnail_height', width_field='thumbnail_width')
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = Course.objects.get_max_order() + 1
        super(Course, self).save(*args, **kwargs)

    class Meta:
        ordering = ['order', ]
        get_latest_by = 'order'

    def __init__(self, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name
