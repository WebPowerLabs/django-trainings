from django.contrib import admin
from resources.models import Resource
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name', '_order']
    list_filter = ['lesson', 'type']

admin.site.register(Resource, ResourceAdmin)
