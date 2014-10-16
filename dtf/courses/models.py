from django.db import models
from django_extensions.db.fields import AutoSlugField, UUIDField
from django.conf import settings
from courses.managers import (CourseManager, CourseHistoryManager,
                              CourseFavouriteManager)
from polymorphic import PolymorphicModel
from django.db.models import permalink
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from utils.search import EsClient


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

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)


class Course(Content):
    """ Course
    Courses are a series of Lessons
    """

    objects = CourseManager()

    thumbnail = models.ImageField(upload_to='courses/thumbs/%Y/%m/%d',
                height_field='thumbnail_height', width_field='thumbnail_width',
                blank=True, null=True)
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    force_progess = models.BooleanField(default=False, 
                    help_text='Force users to complete lessons in order?')
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

    @permalink
    def get_absolute_url(self):
        return 'courses:detail', (), {'slug': self.slug}


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


@receiver(post_save, sender=Course)
def index_es_doc(instance, **kwarg):
    EsClient(instance).index()


@receiver(post_delete, sender=Course)
def delete_es_doc(instance, **kwarg):
    EsClient(instance).delete()
