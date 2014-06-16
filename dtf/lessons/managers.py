from django.db import models
from django.core.urlresolvers import reverse


class LessonManager(models.Manager):
    def published(self):
        return self.filter(published=True)

    def get_list(self, user=None):
        """
        Returns object list all() if user is staff or published() if not.
        """
        if user and user.is_staff:
            return self.all()
        return self.published().filter(course__published=True)

    def get_next_url(self, obj, tag_id=None, course_id=None, user=None):
        """
        Receive Lesson instance and returns URL to next Lesson object.
        """
        lessons = self.get_list(user)
        if tag_id:
            lessons = lessons.filter(tags=tag_id,
                                     created__lt=obj.created).order_by(
                                                              '-created')[:1]
        elif course_id:
            lessons = lessons.filter(course_id=course_id,
                                _order__gt=obj._order).order_by('_order')[:1]
        else:
            lessons = lessons.filter(created__lt=obj.created).order_by(
                                                              '-created')[:1]
        if lessons:
            return reverse('lessons:detail', kwargs={'slug': lessons[0].slug})
        return None

    def get_prev_url(self, obj, tag_id=None, course_id=None, user=None):
        """
        Receive Lesson instance and returns URL to previous Lesson object.
        """
        lessons = self.get_list(user)
        if tag_id:
            lessons = lessons.filter(tags=tag_id,
                                     created__gt=obj.created).order_by(
                                                                'created')[:1]
        elif course_id:
            lessons = lessons.filter(course_id=course_id,
                                       _order__lt=obj._order).order_by(
                                                                '-_order')[:1]
        else:
            lessons = lessons.filter(created__gt=obj.created).order_by(
                                                                'created')[:1]
        if lessons:
            return reverse('lessons:detail', kwargs={'slug': lessons[0].slug})
        return None
