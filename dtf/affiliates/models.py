from django.db import models

from django_extensions.db.fields import AutoSlugField

from .managers import AffiliateManager, PartnerProductManager


class Zip(models.Model):
    affiliate = models.ForeignKey("Affiliate")
    postal_code = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return u'{}'.format(self.postal_code)


class Affiliate(models.Model):
    code = models.CharField(max_length=100, unique=True)
    url = models.URLField(blank=True, null=True)

    objects = AffiliateManager()

    def __unicode__(self):
        return u'{}'.format(self.code)


class PartnerProduct(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='courses/thumbs/%Y/%m/%d',
                height_field='thumbnail_height', width_field='thumbnail_width')
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    partner = models.ForeignKey("Partner", related_name='products')
    link = models.URLField(verbose_name='Affiliate Link')

    objects = PartnerProductManager()

    def __unicode__(self):
        return u'{}'.format(self.name)

    class Meta:
        ordering = ['_order']
        get_latest_by = '_order'
        order_with_respect_to = 'partner'


class Partner(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='courses/thumbs/%Y/%m/%d',
                height_field='thumbnail_height', width_field='thumbnail_width')
    thumbnail_height = models.CharField(max_length=255, blank=True)
    thumbnail_width = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.name)
