from django.db import models

from profiles.models import InfusionsoftProfile

class AffiliateManager(models.Manager):

    def sign_up_affiliate_user_with_code(self, user, code):

        profile = InfusionsoftProfile.objects.get_or_create(user=user)[0]
        # create or update a user with referral code on infusionsoft
        profile.update_profile(referral_code=code)



    def sign_up_affiliate_user_with_zip(self, user):
        affiliate = self.filter(zip__postal_code=user.postal_code)
        if len(affiliate):
            self.sign_up_affiliate_user_with_code(user, affiliate[0].code)




class PartnerProductManager(models.Manager):

    def active(self):
        return self.filter(active=True)