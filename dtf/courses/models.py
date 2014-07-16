from django.db import models
from django_extensions.db.fields import AutoSlugField, UUIDField
from django.conf import settings
from courses.managers import (CourseManager, CourseHistoryManager,
                              CourseFavouriteManager)
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from polymorphic import PolymorphicModel


class Content(PolymorphicModel):
    """
    Base model for Course, Lesson, Resource
    """

    id = UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(blank=True,
        help_text='a brief summary of this course')
    published = models.BooleanField(default=False,
                            help_text='users will only see published courses')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='courses/thumbs/%Y/%m/%d',
                height_field='thumbnail_height', width_field='thumbnail_width')
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)


class Course(Content):
    """ Course
    Courses are a series of Lessons
    """

    objects = CourseManager()

    order = models.IntegerField(editable=False)

    def save(self, *args, **kwargs):
        if self.order is None:
            try:
                self.order = Course.objects.get_max_order() + 1
            except TypeError:
                self.order = 0
        super(Course, self).save(*args, **kwargs)

    class Meta:
        ordering = ['order', ]
        get_latest_by = 'order'

    def __init__(self, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        site = Site.objects.get(pk=settings.SITE_ID)
        return 'http://{0}{1}'.format(site.domain, reverse('courses:detail',
                                                kwargs={'slug': self.slug}))


class History(models.Model):
    """
    For storing history.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'History'


class Favourite(models.Model):
    """
    For storing favourites.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']


class CourseHistory(History):
    objects = CourseHistoryManager()

    course = models.ForeignKey('Course')

    class Meta:
        verbose_name_plural = 'Course History'


class CourseFavourite(Favourite):
    objects = CourseFavouriteManager()
    course = models.ForeignKey('Course')

    class Meta:
        verbose_name_plural = 'Course Favourites'
