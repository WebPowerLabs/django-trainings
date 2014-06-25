from django.db import models

from djnfusion import server, key
from courses.models import Course
from django.conf import settings
from jsonfield import JSONField
# TODO: change to this. Currently doesnt work. may have something to do with
# the server not in __init__
# from packages.providers.infusionsoft import server, key


class Package(models.Model):
    """
    Base for package classes
    """
    name = models.CharField(max_length=255, blank=True)
    course = models.ManyToManyField(Course)

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
    data = JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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

    def sync(self):
        sync_data = self._get_sync_data()
        if sync_data:
            self = InfusionsoftPackage(**sync_data)
            self.save()

    def _get_sync_data(self):
        provider_data = self._get_provider_data()
        if provider_data:remote_id
            package_data = dict({
                "id": self.id,
                "pk": self.pk,
                "action_set_id": self.action_set_id,
                "name": self.name,
                })
            prefix = "infusionsoft"
            for _value in provider_data:
                package_data['_'.join([prefix, _value])] = provider_data[_value]
            return package_data

    def _get_provider_data(self):
        if self.product_id:
            results = server.DataService.findByField(key, "SubscriptionPlan",
                10, 0, "productid", self.product_id,
                ["Id", "ProductId", "Cycle", "Frequency", "PreAuthorizeAmount",
                "Prorate", "Active", "PlanPrice"]);
            return results[0]

    def cancel_subscription(self, contactId, actionSetId):
        results = server.ContactService.runActionSequence(key, contactId,
                                                          actionSetId)
        return results
