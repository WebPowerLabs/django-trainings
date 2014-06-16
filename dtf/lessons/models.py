from django.db import models
from django_extensions.db.fields import AutoSlugField, UUIDField
from django.conf import settings
# import positions
from lessons.managers import LessonManager


class Lesson(models.Model):
    """ Lesson
    A series of Lessons makes up a course. Lessons contain instructions,
    a video, and multiple resources/homework resources.
    """
    objects = LessonManager()

    id = UUIDField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(blank=True,
        help_text='a brief summary of this lesson')
    published = models.BooleanField(default=False,
        help_text='users will only see published lessons')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # order = positions.PositionField()
    thumbnail = models.ImageField(upload_to='lessons/thumbs/%Y/%m/%d',
        height_field='thumbnail_height', width_field='thumbnail_width')
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    video = models.FileField(upload_to='lessons/videos/%Y/%m/%d', blank=True)
    homework = models.TextField(blank=True)
    course = models.ForeignKey('courses.Course')
    tags = models.ManyToManyField('tags.Tag', null=True, blank=True)

    def save(self, *args, **kwargs):
        order = None
        if not self.pk:
            order = self.course.get_lesson_order()
        super(Lesson, self).save(*args, **kwargs)
        if order:
            order.append(self.pk)
            self.course.set_lesson_order(order)

    class Meta:
        ordering = ['_order']
        get_latest_by = '_order'
        order_with_respect_to = 'course'

    def __init__(self, *args, **kwargs):
        super(Lesson, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_resource(self, user):
        return self.resource_set.get_list(user).filter(type='resource')

    def get_homework(self, user):
        return self.resource_set.get_list(user).filter(type='homework')


class LessonHistory(models.Model):
    """
    For storing history.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey('Lesson')

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Lesson history'


class LessonFavourite(models.Model):
    """
    For storing favourites.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    lesson = models.ForeignKey('Lesson')

    class Meta:
        ordering = ['-created']
