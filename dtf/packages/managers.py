# -*- coding: utf-8 -*-
from httplib import CannotSendRequest

from django.db import models
from django.conf import settings

from djnfusion import server, key
from django.db.models import Q


class PackageManager(models.Manager):
    def get_for_content(self, content):
        """
        Receive content object and returns all available packages for it.
        """
        return self.filter(Q(lessons=content.lesson) |
                           Q(courses=content.lesson.course)).distinct()


class PackagePurchaseManager(models.Manager):

    def purchased(self, user=None):
        return self.filter(user=user, status=1)


class InfusionsoftPackageManager(models.Manager):

    def sync(self, **kwargs):
        """ 
        Syncs with infusionsoft api
        arguments:
        """
        product = kwargs.get("product")
        results = server.DataService.findByField(key, "SubscriptionPlan",
            10, 0, "productid", product, ["Id", "ProductId", "Cycle",
            "Frequency", "PreAuthorizeAmount", "Prorate", "Active", "PlanPrice"]);
        return results


class InfusionsoftTagManager(models.Manager):

    def create(self, *args, **kwargs):
        """
        Creates a new tag using info from infusionsoft
        prevents tags from being created that don't exist in infusionsoft
        by overriding the objects create method
        """
        remote_id = kwargs.get("remote_id") if kwargs.get("remote_id") else None
        if remote_id:
            # remote id provided - connect to infusionsoft server
            sync_data = self._get_sync_data(remote_id)
        if sync_data:
            return super(InfusionsoftTagManager, self).create(**sync_data)

    def create_sync(self, **kwargs):
        """
        Creates a new tag using info from infusionsoft
        """
        remote_id = kwargs.get("remote_id") if kwargs.get("remote_id") else None
        if remote_id:
            # remote id provided - connect to infusionsoft server
            sync_data = self._get_sync_data(remote_id) if self.remote_id else kwargs
        if sync_data:

            return self.create(**sync_data)

    def by_user(self, user=None):
        """
        Returns tags a user has from the infusionsoft server
        **kwargs
        user: user instance or email
        """
        tag_str = self._get_provider_tags_data_for_user(user)
        tag_ids = [int(tag_id) for tag_id in tag_str.split(",")] if tag_str else []
        tags = self.filter(remote_id__in=tag_ids) if len(tag_ids) else self.none()
        return tags

    def _get_sync_data(self, remote_id=None):
        """
        Converts remote data keys into model keys
        """
        provider_data = self._get_provider_data(remote_id)
        if provider_data:
            tag_data = dict({
                "remote_id": provider_data["Id"],
                "group_category_id": provider_data["GroupCategoryId"],
                "group_name": provider_data["GroupName"],
                "group_description": provider_data["GroupDescription"],
                })
            return tag_data

    def _get_provider_data(self, remote_id=None):
        """
        Gets data from an id lookup over infusionsoft server
        """
        if remote_id:
            results = server.DataService.findByField(key, "ContactGroup",
                10, 0, "id", remote_id,
                ["Id", "GroupCategoryId", "GroupName", "GroupDescription"]);
            # sync data is None if an empty array
            return results[0] if len(results) else None

    def _get_provider_users_data(self, remote_id=None):
        """
        Returns array of user infusionsoftprofile remote_ids associated with a tag
        """
        if remote_id:
            results = server.DataService.findByField(key, "ContactGroupAssign",
                10, 0, "GroupId", remote_id,
                ["ContactId", ]);
            # sync data is None if an empty array
            return [user['ContactId'] for user in results]

    def _get_provider_tags_data_for_user(self, user=None):
        """
        Gets a users tags from infusionsoft and returns a string
        **kwargs
        user: user instance
        """
        if user and settings.DJNFUSION_COMPANY and settings.DJNFUSION_API_KEY:
            # try getting users infusionsoft id, use email as backup
            _key = "Id" if user.infusionsoftprofile else "email"
            _value = user.infusionsoftprofile.get_remote_id if user.infusionsoftprofile else user.email
            if _key and _value:
                try:
                    # if they have an infusionsoft profile this should work
                    results = server.DataService.findByField(key, "Contact",
                        10, 0, _key, _value,
                        ["Groups", ]);
                except CannotSendRequest:
                    results = (None,)
            try:
                return_results = results[0]["Groups"] if len(results) else None
            except KeyError:
                return_results = None
            return  return_results
