from django.contrib import admin

from .models import FacebookProfile, History, InfusionsoftProfile
from profiles.models import Favourite
# 				    PackageProfile


class HistoryAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'created', 'content_type']
    list_filter = ['user']


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'created', 'content_type']
    list_filter = ['user']

admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(FacebookProfile)
admin.site.register(InfusionsoftProfile)
# admin.site.register(PackageProfile)
