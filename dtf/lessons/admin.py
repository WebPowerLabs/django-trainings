from django.contrib import admin
from lessons.models import Lesson, LessonHistory, LessonFavourite
from resources.models import Resource


class ResourceInLine(admin.TabularInline):
    model = Resource


class LessonAdmin(admin.ModelAdmin):
    inlines = [ResourceInLine]
    list_filter = ['course']
    list_editable = ['published']
    list_display = ['name', 'published', '_order']


class LessonHistoryAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'created', 'is_active']
    list_filter = ['created']
    list_editable = ['is_active']


class LessonFavouriteAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'created', 'is_active']
    list_filter = ['user']
    list_editable = ['is_active']

admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonHistory, LessonHistoryAdmin)
admin.site.register(LessonFavourite, LessonFavouriteAdmin)




