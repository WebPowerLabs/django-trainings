from django.contrib import admin

from .models import (CourseProfile, LessonProfile, FacebookProfile, 
	InfusionsoftProfile,) #PackageProfile


admin.site.register(CourseProfile)
admin.site.register(LessonProfile)
admin.site.register(FacebookProfile)
admin.site.register(InfusionsoftProfile)
#admin.site.register(PackageProfile)