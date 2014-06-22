from django.contrib import admin

from .models import FacebookProfile, InfusionsoftProfile
from profiles.models import InstructorProfile
# 				    PackageProfile

admin.site.register(FacebookProfile)
admin.site.register(InfusionsoftProfile)
admin.site.register(InstructorProfile)
# admin.site.register(PackageProfile)
