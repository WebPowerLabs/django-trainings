from django.db import models


class FeatureManager(models.Manager):
    def active(self):
        return self.filter(active=True)
