from django.contrib import admin
from resources.models import Resource


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['lesson', 'type']

admin.site.register(Resource, ResourceAdmin)

