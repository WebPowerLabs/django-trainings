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
    list_display = ['lesson', 'user', 'created']
    list_filter = ['created']


class LessonFavouriteAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'created']
    list_filter = ['user']

admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonHistory, LessonHistoryAdmin)
admin.site.register(LessonFavourite, LessonFavouriteAdmin)




