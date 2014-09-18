from django.db import models
from django.db.models import Q, Count, Max
from django.core.urlresolvers import reverse
from profiles.models import InstructorProfile
from polymorphic.manager import PolymorphicManager


class LessonManager(PolymorphicManager):

    def completed(self, user, course=None):

        lessons = self.purchased(user).filter(lessoncomplete__user=user, 
                                              lessoncomplete__is_complete=True)
        if course:
            return lessons.filter(course=course)
        return lessons

    def get_current(self, user, course):
        completed_order = self.completed(user, course=course
                                         ).aggregate(
                                         Max('_order'))['_order__max']
        if not completed_order and completed_order != 0:
            completed_order = -1
        # list of lessons for course that have not been completed
        not_completed = self.published().filter(
                                 _order__gt=completed_order,
                                 course=course,
                                 )
        # if there are uncompleted lessons
        if len(not_completed):
            return not_completed[0] # return the next lesson
        # if there are no uncomplete lessons, the course is complete
        else:

            return self.completed(user, course=course).order_by('-_order')[0]

    def published(self):
        return self.filter(published=True, course__published=True)

    def purchased(self, user):
        return self.annotate(Count('package'), Count('course__package')
                             ).filter(
                              Q(package__packagepurchase__user=user,
                                package__packagepurchase__status=1) |
                              Q(course__package__packagepurchase__user=user,
                                course__package__packagepurchase__status=1) |
                              Q(package__count=0, course__package__count=0),
                              published=True, course__published=True
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
                return self.all()
        return self.published()

    def get_next_url(self, obj, tag_id=None, course_id=None, purchased=None,
                     user=None):
        """
        Receive Lesson instance and returns URL to next Lesson object.
        """
        lessons = self.get_list(user)
        if purchased:
            lessons = self.purchased(user)
        if tag_id:
            lessons = lessons.filter(tags=tag_id, created__lt=obj.created
                                     ).order_by('-created')[:1]
        elif course_id:
            lessons = lessons.filter(course_id=course_id, _order__gt=obj._order
                                     ).order_by('_order')[:1]
        else:
            lessons = lessons.filter(created__lt=obj.created
                                     ).order_by('-created')[:1]
        if lessons:
            return reverse('lessons:detail', kwargs={'slug': lessons[0].slug})
        return None

    def get_prev_url(self, obj, tag_id=None, course_id=None, purchased=None,
                     user=None):
        """
        Receive Lesson instance and returns URL to previous Lesson object.
        """
        lessons = self.get_list(user)
        if purchased:
            lessons = self.purchased(user)
        if tag_id:
            lessons = lessons.filter(tags=tag_id, created__gt=obj.created
                                     ).order_by('created')[:1]
        elif course_id:
            lessons = lessons.filter(course_id=course_id, _order__lt=obj._order
                                     ).order_by('-_order')[:1]
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
