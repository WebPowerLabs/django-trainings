from django.db import models
from django.core.urlresolvers import reverse
from djnfusion import server, key

from django.conf import settings
from jsonfield import JSONField

# TODO: change to this. Currently doesnt work. may have something to do with
# the server not in __init__
# from packages.providers.infusionsoft import server, key
from .managers import InfusionsoftTagManager, PackagePurchaseManager
from packages.managers import PackageManager


def remove_unused(_dict):
    return_dict = {}
    for _key, _value in _dict.iteritems():
        if _value:
            return_dict[_key] = _value
    return return_dict


def setdictattrs(obj, _dict):
    _dict = remove_unused(_dict)
    for _key, _value in _dict.iteritems():
        setattr(obj, _key, _value)


class Package(models.Model):
    """
    Base for package classes
    """
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField("courses.Course", null=True, blank=True)
    lessons = models.ManyToManyField("lessons.Lesson", null=True, blank=True)
    groups = models.ManyToManyField("facebook_groups.FacebookGroup", null=True,
                                    blank=True)

    objects = PackageManager()

    def __unicode__(self):
        return u'{}'.format(self.name if self.name else 'Package')

    def get_absolute_url(self):
        return reverse('packages:detail', kwargs={'pk': self.pk})


class PackagePurchase(models.Model):
    """
    User's purchased packages.
    """
    INACTIVE = 0
    ACTIVE = 1
    EXPIRED = 2
    STATUS_CHOICES = [
                      [INACTIVE, 'Inactive'],
                      [ACTIVE, 'Active'],
                      [EXPIRED, 'Expired'],
                      ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    package = models.ForeignKey('Package')
    status = models.IntegerField(choices=STATUS_CHOICES, default=INACTIVE)
    data = JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PackagePurchaseManager()

    def __unicode__(self):
        return u'{0} => {1}'.format(self.user, self.package)

    def set_status(self, status):
        self.status = status
        self.save()


class InfusionsoftPackage(Package):
    """
    Package with infusionsoft api hooks
    """
    subscription_id = models.TextField(blank=True, null=True)
    product_id = models.TextField(blank=True, null=True)
    cycle = models.TextField(blank=True, null=True)
    frequency = models.TextField(blank=True, null=True)
    pre_authorize_amount = models.TextField(blank=True, null=True)
    prorate = models.TextField(blank=True, null=True)
    active = models.TextField(blank=True, null=True)
    plan_price = models.TextField(blank=True, null=True)
    product_price = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    action_set_id = models.TextField(blank=True, null=True)
    tag = models.OneToOneField("InfusionsoftTag", blank=True, null=True)
    purchase_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        sync_data = self._get_sync_data(product_id=self.product_id) if self.product_id else None
        if sync_data:
            setdictattrs(self, sync_data)
        return super(InfusionsoftPackage, self).save(*args, **kwargs)

    def sync(self):
        sync_data = self._get_sync_data()
        if sync_data:
            setdictattrs(self, sync_data)

        self.save()

    def _get_sync_data(self, product_id=None):
        subscription_data = self._get_subscription_data(product_id)
        product_data = self._get_product_data(product_id)
        if subscription_data and product_data:
            package_data = dict({
                "id": self.id,
                "pk": self.pk,
                "action_set_id": self.action_set_id,
                "name": product_data.get("ProductName"),
                "subscription_id": subscription_data.get("Id"),
                "product_id": subscription_data.get("ProductId"),
                "cycle": subscription_data.get("Cycle"),
                "frequency": subscription_data.get("Frequency"),
                "prorate": subscription_data.get("Prorate"),
                "active": subscription_data.get("Active"),
                "plan_price": subscription_data.get("PlanPrice"),
                "product_price": product_data.get("ProductPrice"),
                "description": product_data.get("Description"),
                "status": product_data.get("Status"),
                })
        elif product_data:
            # product but not subscription
            package_data = dict({
                "id": self.id,
                "pk": self.pk,
                "action_set_id": self.action_set_id,
                "name": product_data.get("ProductName"),
                "product_id": product_data.get("Id"),
                "product_price": product_data.get("ProductPrice"),
                "description": product_data.get("Description"),
                "status": product_data.get("Status"),
                })
        return package_data if package_data else None

    def _get_subscription_data(self, product_id=None):
        product_id = product_id if product_id else self.product_id
        if product_id:
            results = server.DataService.findByField(key, "SubscriptionPlan",
                10, 0, "productid", product_id,
                ["Id", "ProductId", "Cycle", "Frequency", "PreAuthorizeAmount",
                "Prorate", "Active", "PlanPrice"]);
            return results[0] if len(results) else None

    def _get_product_data(self, product_id=None):
        product_id = product_id if product_id else self.product_id
        if product_id:
            results = server.DataService.findByField(key, "Product",
                10, 0, "id", product_id,
                ["Id", "ProductName", "ProductPrice", "Description",
                "Status", "IsPackage"]);
            return results[0] if len(results) else None

    def cancel_subscription(self, contactId, actionSetId):
        results = server.ContactService.runActionSequence(key, contactId,
                                                          actionSetId)
        return results

    @property
    def price(self):
        return self.plan_price if self.plan_price else self.product_price


class InfusionsoftTag(models.Model):
    '''
    Infusionsoft Tag (ContactGroup)
    '''
    remote_id = models.TextField()
    group_category_id = models.TextField(blank=True, null=True)
    group_name = models.TextField(blank=True, null=True)
    group_description = models.TextField(blank=True, null=True)

    objects = InfusionsoftTagManager()

    def __unicode__(self):
        return u'{}'.format(self.group_name if self.group_name else u'InfusionsoftTag Object')

    def save(self, *args, **kwargs):
        remote_id = kwargs.get('remote_id') if kwargs.get('remote_id') else self.remote_id
        sync_data = self._get_sync_data(remote_id=remote_id) if remote_id else None
        if sync_data:
            obj = InfusionsoftTag(**sync_data)
            return super(InfusionsoftTag, obj).save(*args, **kwargs)
        else:
            return super(InfusionsoftTag, self).save(*args, **kwargs)

    def sync(self):
        sync_data = self._get_sync_data()
        if sync_data:
            self = InfusionsoftTag(**sync_data)
            self.save()

    def _get_sync_data(self, remote_id=None):
        provider_data = self._get_provider_data(remote_id)
        if provider_data:
            tag_data = dict({
                "id": self.id,
                "pk": self.pk,
                "remote_id": provider_data.get("Id"),
                "group_category_id": provider_data.get("GroupCategoryId"),
                "group_name": provider_data.get("GroupName"),
                "group_description": provider_data.get("GroupDescription"),
                })
            return tag_data

    def _get_provider_data(self, remote_id=None):
        remote_id = remote_id if remote_id else self.remote_id
        if remote_id:
            results = server.DataService.findByField(key, "ContactGroup",
                10, 0, "id", remote_id,
                ["Id", "GroupCategoryId", "GroupName", "GroupDescription"]);
            return results[0] if len(results) else None
