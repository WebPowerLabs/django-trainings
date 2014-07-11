from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from profiles.models import InstructorProfile
from polymorphic.manager import PolymorphicManager


class LessonManager(PolymorphicManager):
    def published(self):
        return self.filter(published=True)

    def purchased(self, user):
        if user and user.is_authenticated():
            try:
                instructor = user.instructorprofile
            except InstructorProfile.DoesNotExist:
                instructor = False
            if user.is_staff or instructor:
                return self.filter(Q(published=True) | Q(owner=user))
        return self.filter(Q(package__packagepurchase__user=user) |
                           Q(course__package__packagepurchase__user=user)
                           ).distinct()

    def owned(self, user):
        return self.filter(owner=user)

    def get_list(self, user=None):
        """
        Returns object list all() if user is staff/instructor
        or published() if not.
        """
        if user and user.is_authenticated():
            try:
                instructor = user.instructorprofile
            except InstructorProfile.DoesNotExist:
                instructor = False
            if user.is_staff or instructor:
                return self.filter(Q(published=True) | Q(owner=user))
        return self.published().filter(course__published=True)  # course is published too

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


class LessonHistoryManager(models.Manager):
    def active(self, user):
        return self.filter(is_active=True, user=user)


class LessonFavouriteManager(models.Manager):
    def active(self, user):
        return self.filter(is_active=True, user=user)
