from django.db import models
from django.core.urlresolvers import reverse


class LessonManager(models.Manager):
    def get_next_url(self, obj, tag_id=None, course_id=None):
        lessons = self.all()
        if tag_id:
            lessons = lessons.filter(tags=tag_id,
                                     created__gt=obj.created).order_by(
                                                                    'created')
            if lessons:
                return reverse('lessons:detail', kwargs={
                                                      'slug': lessons[0].slug})
        elif course_id:
            lessons = lessons.filter(course_id=course_id,
                                     order__gt=obj.order).order_by('order')
            if lessons:
                return reverse('lessons:detail', kwargs={
                                                      'slug': lessons[0].slug})
        else:
            lessons = self.filter(created__gt=obj.created).order_by('created')
            if lessons:
                return reverse('lessons:detail', kwargs={
                                                      'slug': lessons[0].slug})
        return None

    def get_prev_url(self, obj, tag_id=None, course_id=None):
        lessons = self.all()
        if tag_id:
            lessons = lessons.filter(tags=tag_id,
                                     created__lt=obj.created).order_by(
                                                                     '-created')
            if lessons:
                return reverse('lessons:detail', kwargs={
                                                      'slug': lessons[0].slug})
        elif course_id:
            lessons = lessons.filter(course_id=course_id,
                                     order__lt=obj.order).order_by('-order')
            if lessons:
                return reverse('lessons:detail', kwargs={
                                                      'slug': lessons[0].slug})
        else:
            lessons = self.filter(created__lt=obj.created).order_by('-created')
            if lessons:
                return reverse('lessons:detail', kwargs={
                                                      'slug': lessons[0].slug})
        return None
