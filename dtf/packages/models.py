from django.db import models

from djnfusion import server, key
# TODO: change to this. Currently doesnt work. may have something to do with 
# the server not in __init__
# from packages.providers.infusionsoft import server, key


class PackageAbstractModel(models.Model):
    """
    Base for package classes
    """
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'{}'.format(self.name)


class InfusionsoftPackage(PackageAbstractModel):
    """
    Package with infusionsoft api hooks
    """
    infusionsoft_Id = models.TextField(blank=True)
    infusionsoft_ProductId = models.TextField(blank=True)
    infusionsoft_Cycle = models.TextField(blank=True)
    infusionsoft_Frequency = models.TextField(blank=True)
    infusionsoft_PreAuthorizeAmount = models.TextField(blank=True)
    infusionsoft_Prorate = models.TextField(blank=True)
    infusionsoft_Active = models.TextField(blank=True)
    infusionsoft_PlanPrice = models.TextField(blank=True)
    infusionsoft_actionSetId = models.TextField(blank=True)

    def sync(self):
        sync_data = self._get_sync_data()
        if sync_data:
            self = InfusionsoftPackage(**sync_data)
            self.save()

    def _get_sync_data(self):
        provider_data = self._get_provider_data()
        if provider_data:
            package_data = dict({
                "id": self.id, 
                "pk": self.pk, 
                "infusionsoft_actionSetId": self.infusionsoft_actionSetId,
                "name": self.name,
                })
            prefix = "infusionsoft"
            for _value in provider_data:
                package_data['_'.join([prefix, _value])] = provider_data[_value]
            return package_data

    def _get_provider_data(self):
        if self.infusionsoft_ProductId:
            results = server.DataService.findByField(key, "SubscriptionPlan", 
                10, 0, "productid", self.infusionsoft_ProductId, 
                ["Id", "ProductId", "Cycle", "Frequency", "PreAuthorizeAmount", 
                "Prorate", "Active", "PlanPrice"]);
            return results[0]

    def cancel_subscription(self, contactId, actionSetId):
        results = server.ContactService.runActionSequence(key, contactId, actionSetId)
        return results

