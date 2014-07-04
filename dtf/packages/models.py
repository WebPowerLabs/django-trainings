from django.db import models

from djnfusion import server, key

from django.conf import settings
from jsonfield import JSONField

# TODO: change to this. Currently doesnt work. may have something to do with
# the server not in __init__
# from packages.providers.infusionsoft import server, key
from .managers import InfusionsoftTagManager, PackagePurchaseManager


class Package(models.Model):
    """
    Base for package classes
    """
    name = models.CharField(max_length=255, blank=True)
    courses = models.ManyToManyField("courses.Course")
    lessons = models.ManyToManyField("lessons.Lesson")

    def __unicode__(self):
        return u'{}'.format(self.name)


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
    remote_id = models.TextField(blank=True)
    product_id = models.TextField(blank=True)
    cycle = models.TextField(blank=True)
    frequency = models.TextField(blank=True)
    pre_authorize_amount = models.TextField(blank=True)
    prorate = models.TextField(blank=True)
    active = models.TextField(blank=True)
    plan_price = models.TextField(blank=True)
    action_set_id = models.TextField(blank=True)
    tag = models.OneToOneField("InfusionsoftTag", blank=True, null=True)

    def sync(self):
        sync_data = self._get_sync_data()
        if sync_data:
            self = InfusionsoftPackage(**sync_data)
            self.save()

    def _get_sync_data(self):
        provider_data = self._get_provider_data()
        product_data = self._get_product_data()
        if provider_data:
            package_data = dict({
                "id": self.id,
                "pk": self.pk,
                "action_set_id": self.action_set_id,
                "name": self.name,
                "remote_id": provider_data["Id"],
                "product_id": provider_data["ProductId"],
                "cycle": provider_data["Cycle"],
                "frequency": provider_data["Frequency"],
                "prorate": provider_data["Prorate"],
                "active": provider_data["Active"],
                "plan_price": provider_data["PlanPrice"]
                })
            return package_data

    def _get_provider_data(self):
        if self.product_id:
            results = server.DataService.findByField(key, "SubscriptionPlan",
                10, 0, "productid", self.product_id,
                ["Id", "ProductId", "Cycle", "Frequency", "PreAuthorizeAmount",
                "Prorate", "Active", "PlanPrice"]);
            return results[0]

    def _get_product_data(self):
        if self.product_id:
            results = server.DataService.findByField(key, "Product",
                10, 0, "id", self.product_id,
                ["Id", "ProductName", "productPrice", "ShortDescription", "Description",
                "LargeImage", "Status", "IsPackage"]);
            return results[0]

    def cancel_subscription(self, contactId, actionSetId):
        results = server.ContactService.runActionSequence(key, contactId,
                                                          actionSetId)
        return results
    


class InfusionsoftTag(models.Model):
    '''
    Infusionsoft Tag (ContactGroup)
    '''
    remote_id = models.TextField(blank=True)
    group_category_id = models.TextField(blank=True)
    group_name = models.TextField(blank=True)
    group_description = models.TextField(blank=True)

    objects = InfusionsoftTagManager()

    def __unicode__(self):
        return self.group_name if self.group_name else self.pk

    def sync(self):
        sync_data = self._get_sync_data()
        if sync_data:
            self = InfusionsoftPackage(**sync_data)
            self.save()

    def _get_sync_data(self):
        provider_data = self._get_provider_data()
        if provider_data:
            tag_data = dict({
                "id": self.id,
                "pk": self.pk,
                "remote_id": provider_data["Id"],
                "group_category_id": provider_data["GroupCategoryId"],
                "group_name": provider_data["GroupName"],
                "group_description": provider_data["GroupDescription"],
                })
            return tag_data

    def _get_provider_data(self):
        if self.remote_id:
            results = server.DataService.findByField(key, "ContactGroup",
                10, 0, "id", self.remote_id,
                ["Id", "GroupCategoryId", "GroupName", "GroupDescription"]);
            return results[0]
