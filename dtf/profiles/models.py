from django.db import models
from django.conf import settings

from djnfusion import server, key

from packages.models import InfusionsoftTag, PackagePurchase

# class PackageProfile(models.Model):
#    '''
#    for storing information about Packages
#    '''
#    user = models.OneToOneField(settings.AUTH_USER_MODEL)
#    packages = models.ManyToManyField("packages.Package")


class FacebookProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    fb_uid = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.username


class InfusionsoftProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    remote_id = models.TextField(blank=True)
    tags = models.ManyToManyField(InfusionsoftTag,
        related_name="infusionsoft_profiles", blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    @property
    def get_remote_id(self):
        if not self.remote_id:
            self.update_profile()
        return self.remote_id if self.remote_id else None


    def update_tags(self):
        """
        updates a profiles tags from the infusionsoft server
        """
        # get infusionsofts tags from thier server and find the instances in our db
        tags = InfusionsoftTag.objects.by_user(self.user)
        # get all active purchase for profile.user
        active_purchases = PackagePurchase.objects.filter(user__id=self.user_id,
            package__infusionsoftpackage__tag_id__in=[tag.id for tag in self.tags.all()], status=1)  # 1 == Active

        for tag in self.tags.all():
            # loop through profile's tags
            if tag not in tags:
                # profile has tag that was removed on infusionsoft, remove tag
                self.tags.remove(tag)
                # set past_purchases of this tag to expired

                expired = active_purchases.filter(package__infusionsoftpackage__tag_id=tag.id)
                for purchase in expired:
                    purchase.status = 2  # 2 == Expired
                    purchase.save()


        for tag in tags:
            # loop through infusionsoft's tags
            if tag not in self.tags.all():
                # profile does not have tag on infusionsoft, add tag
                self.tags.add(tag)
                # create a new package purchase for the tags infusionsoft package
                PackagePurchase.objects.create(
                    user=self.user, package=tag.infusionsoftpackage, status=1)  # 1 == Active

        return self.save()

    def update_profile(self):
        """
        updates profile fields from infusionsoft server
        """
        provider_data = self._get_provider_data()
        if len(provider_data):
            self.remote_id = provider_data["Id"]
            return self.save()


    def _get_provider_data(self):
        """
        Gets a profiles user's data from infusionsoft
        """
        results = server.DataService.findByField(key, "Contact",
            10, 0, "email", self.user.email,
            ["Id", ]);
        return results[0] if len(results) else None


class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.user.username


from allauth.account.signals import user_logged_in
from django.dispatch import receiver


# @receiver(user_logged_in)
def infusionsoft_sync_user(sender, **kwargs):
    user = kwargs['user']
    profile = InfusionsoftProfile.objects.get_or_create(user=user)[0]
    profile.update_tags()
    print profile.tags.all()




