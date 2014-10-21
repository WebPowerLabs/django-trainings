from django.db import models


class EtfarManager(models.Manager):

    def access(self, user):
        conditions = self.filter(active=True)
        conditions_met = self.filter(active=True, 
                                     package__packagepurchase__user=user,
                                    package__packagepurchase__status=1)
        if len(conditions) <= len(conditions_met):
            # user passes
            return True
        elif user.is_staff:
            # user is staff, passes any way
            return True
        # User fails
        return False