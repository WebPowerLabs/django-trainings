from django.db import models
from django.db.models.aggregates import Max


class CourseManager(models.Manager):
    def published(self):
        return self.filter(published=True)

    def get_list(self, user=None):
        """
        Returns object list all() if user is staff or published() if not.
        """
        if user and user.is_staff:
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
