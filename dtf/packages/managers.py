# -*- coding: utf-8 -*-
from django.db import models

from providers.infusionsoft import server, key


class InfusionsoftPackageManager(models.Manager):

    def sync(self, **kwargs):
        """ 
        Syncs with infusionsoft api
        arguments:
        
        """
        product = kwargs.get("product")
        results = server.DataService.findByField(key, "SubscriptionPlan", 10, 0, "productid", product, 
            ["Id", "ProductId", "Cycle", "Frequency", "PreAuthorizeAmount", "Prorate", "Active", "PlanPrice"]);
        return results