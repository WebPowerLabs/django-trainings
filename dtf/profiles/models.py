from django.db import models
from django.conf import settings

from djnfusion import server, key

from packages.models import InfusionsoftTag, PackagePurchase


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    archetype = models.CharField(max_length=255, blank=True, 
                                 verbose_name=u'My Archetype')
    anthem = models.TextField(blank=True, verbose_name=u'My Anthem')
    about = models.TextField(blank=True, verbose_name=u'I am...')
    support = models.TextField(blank=True, 
                               verbose_name=u'I need support in achieving:')

    def __unicode__(self):
        return self.user.username


class UserPrivateProfile(models.Model):
    '''
    Private profile for users. Other users are not able to view this unless
    they are staff
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                related_name='private_profile')
    dream = models.TextField(blank=True,
                             verbose_name=u'My BIG dream is:')

    def __unicode__(self):
        return self.user.username

    def can_view(self, user):
        '''
        Other users are not able to view this unless they are staff
        '''
        return user == self.user or user.is_staff


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
        if settings.DJNFUSION_COMPANY and settings.DJNFUSION_API_KEY:
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
        if not len(results):
            #TODO:FIX THIS java.lang.String ERROR
#            remote_id = server.ContactService.add(key, [
#                {"djUserID": unicode(self.user.id)},
#                {"Email": self.user.email},
#                {"FirstName": self.user.first_name},
#                {"LastName": self.user.last_name}])

#            return {"Id": remote_id}
            return []
        return results[0]


class InstructorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.user.username


from allauth.account.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def infusionsoft_sync_user(sender, **kwargs):
    if settings.DJNFUSION_COMPANY:
        user = kwargs['user']
        profile = InfusionsoftProfile.objects.get_or_create(user=user)[0]
        profile.update_tags()




