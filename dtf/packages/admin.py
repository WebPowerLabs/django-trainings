from django.contrib import admin

from .models import InfusionsoftPackage
from packages.models import Package, PackagePurchase, InfusionsoftTag


class InfusionsoftPackageAdmin(admin.ModelAdmin):
	pass

class InfusionsoftTagAdmin(admin.ModelAdmin):
	pass

admin.site.register(Package)
admin.site.register(PackagePurchase)
admin.site.register(InfusionsoftPackage, InfusionsoftPackageAdmin)
admin.site.register(InfusionsoftTag, InfusionsoftTagAdmin)
