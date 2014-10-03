from django.conf import settings
from django.db import models
from lessons.managers import (LessonManager, LessonHistoryManager,
                              LessonFavouriteManager)
from courses.models import Content, History, Favourite
from django.db.models import permalink
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from utils.search import EsClient
import ntpath
from lessons.tasks import process_video


class Video(models.Model):
    SCHEDULED = 0
    CONVERTED = 1
    CONVERTING = 2
    ERROR = 3

    STATUS_CHOICES = [
              [CONVERTING, 'Converting'],
              [ERROR, 'Error'],
              [SCHEDULED, 'Scheduled'],
              [CONVERTED, 'Converted']
              ]
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=SCHEDULED)
    orig = models.FileField(upload_to='lessons/videos/orig/%Y/%m/%d',
                            null=True, blank=True)
    mp4 = models.FileField(upload_to='lessons/videos/mp4/%Y/%m/%d',
                           null=True, blank=True)
    webm = models.FileField(upload_to='lessons/videos/webm/%Y/%m/%d',
                            null=True, blank=True)
    
    def __unicode__(self):
        return self.filename
    
    @property
    def filename(self):
        return ntpath.basename(self.orig.file.name)

class Lesson(Content):
    """ Lesson
    A series of Lessons makes up a course. Lessons contain instructions,
    a video, and multiple resources/homework resources.
    """
    objects = LessonManager()

    video = models.OneToOneField('Video', blank=True, null=True)
    audio = models.FileField(upload_to='lessons/audio/%Y/%m/%d', blank=True,
                            null=True)
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

    @permalink
    def get_absolute_url(self):
        return 'lessons:detail', (), {'slug': self.slug}

    def can_start(self, user):
        '''
        A user will need to mark previous lessons as completed in order to
        begin new lessons
        '''
        current_lesson_order = Lesson.objects.completed(
                                     user, course=self.course
                                     ).aggregate(models.Max('_order')
                                     )['_order__max']
        if not current_lesson_order and current_lesson_order != 0:
            current_lesson_order = -1
        return self._order <= (current_lesson_order+1)


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


class LessonComplete(models.Model):
    """
    Through model between user and lesson that allows users to check lesson
    as completed.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    lesson = models.ForeignKey('Lesson')
    is_complete = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lesson complete item'
        verbose_name_plural = 'Lesson complete items'


@receiver(post_save, sender=Lesson)
def index_es_doc(instance, **kwarg):
    EsClient(instance).index()


@receiver(post_delete, sender=Lesson)
def delete_es_doc(instance, **kwarg):
    EsClient(instance).delete()

@receiver(post_save, sender=Video)
def convert_video(instance, created, **kwarg):
    if created:
        process_video.delay(instance)
