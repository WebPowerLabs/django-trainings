from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Max
from profiles.models import InstructorProfile
from polymorphic import PolymorphicManager


class CourseManager(PolymorphicManager):
    def published(self):
        return self.filter(published=True)

    def purchased(self, user):
        return self.filter(Q(package__packagepurchase__user=user) |
                           Q(lesson__package__packagepurchase__user=user)
                           ).distinct()

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

    def get_order(self):
        """
        Returns current objects order.
        """
        return list(self.all().order_by('order').values_list('pk', flat=True))

    def set_order(self, order):
        """
        Receives new order for objects and sets it.
        """
        items = self.filter(pk__in=order)
        items = {obj.pk: obj for obj in items}
        for position, pk in enumerate(order):
            items[pk].order = position
            items[pk].save()
        return order

    def get_max_order(self):
        return self.aggregate(max_order=Max('order'))['max_order']


class CourseHistoryManager(models.Manager):
    def active(self, user):
        return self.filter(is_active=True, user=user)


class CourseFavouriteManager(models.Manager):
    def active(self, user):
        return self.filter(is_active=True, user=user)
