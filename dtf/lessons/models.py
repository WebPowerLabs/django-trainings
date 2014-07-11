from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from lessons.managers import (LessonManager, LessonHistoryManager,
                              LessonFavouriteManager)
from courses.models import Content, History, Favourite


class Lesson(Content):
    """ Lesson
    A series of Lessons makes up a course. Lessons contain instructions,
    a video, and multiple resources/homework resources.
    """
    objects = LessonManager()

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
    
    def get_absolute_url(self):
        site = Site.objects.get(pk=settings.SITE_ID)
        return 'http://{0}{1}'.format(site.domain, reverse('lessons:detail',
                                                kwargs={'slug': self.slug}))


class LessonHistory(History):
    """
    For storing history.
    """
    objects = LessonHistoryManager()

    lesson = models.ForeignKey('Lesson')

    class Meta:
        verbose_name_plural = 'Lesson History'


class LessonFavourite(Favourite):
    """
    For storing favourites.
    """
    objects = LessonFavouriteManager()

    lesson = models.ForeignKey('Lesson')

    class Meta:
        verbose_name_plural = 'Lesson Favourites'
