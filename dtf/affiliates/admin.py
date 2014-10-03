from django.contrib import admin

from .models import Zip, Affiliate, PartnerProduct, Partner


class ZipInline(admin.TabularInline):
    model = Zip
    fk_name = 'affiliate'


class AffiliateAdmin(admin.ModelAdmin):
    inlines = [ZipInline,]


class PartnerProductInline(admin.TabularInline):
    model = PartnerProduct
    fk_name = 'partner'


class PartnerAdmin(admin.ModelAdmin):
    inlines = [PartnerProductInline,]
    list_display = ['name', 'active']
    list_editable = ['active',]


admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(Partner, PartnerAdmin)