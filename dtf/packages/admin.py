from django.contrib import admin

from .models import InfusionsoftPackage


class InfusionsoftPackageAdmin(admin.ModelAdmin):
	pass

admin.site.register(InfusionsoftPackage, InfusionsoftPackageAdmin)