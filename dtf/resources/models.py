from django.db import models
from resources.managers import ResourceManager
from courses.models import Content


class Resource(Content):
    """ Resource
    A resource for a lesson. can include a file or just use description.
    Have several fields available incase resource wants its own detailview
    """
    objects = ResourceManager()

    TYPE_CHOICES = (
        ('resource', 'Resource'),
        ('homework', 'Homework'),
        )

    type = models.CharField(choices=TYPE_CHOICES, default='resource',
        max_length=255)
    lesson = models.ForeignKey('lessons.Lesson')
    file = models.FileField(upload_to='resources/files/%Y/%m/%d', blank=True)

    def save(self, *args, **kwargs):
        order = None
        if not self.pk:
            order = self.lesson.get_resource_order()
        super(Resource, self).save(*args, **kwargs)
        if order:
            order.append(self.pk)
            self.lesson.set_resource_order(order)

    class Meta:
        ordering = ['_order', ]
        get_latest_by = '_order'
        order_with_respect_to = 'lesson'

    def __unicode__(self):
        return "{}[{}]".format(self.name, self.type)
