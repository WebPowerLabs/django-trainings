from django.db import models


class ResourceManager(models.Manager):
    def published(self):
        return self.filter(published=True)

    def get_list(self, user=None):
        """
        Returns object list all() if user is staff or published() if not.
        """
        if user and user.is_staff:
            return self.all()
        return self.published()