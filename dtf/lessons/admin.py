from django.contrib import admin
from lessons.models import (Lesson, LessonHistory, LessonFavourite,
                            LessonComplete, Video)
from resources.models import Resource


class ResourceInLine(admin.TabularInline):
    model = Resource
    fk_name = 'lesson'
    template = 'admin/polymorphic_tabular.html'


class LessonAdmin(admin.ModelAdmin):
    inlines = [ResourceInLine]

    list_filter = ['course']
    list_editable = ['published']
    list_display = ['name', 'published', '_order']


class LessonHistoryAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'created', 'is_active']
    list_filter = ['created', 'user', 'lesson']
    list_editable = ['is_active']


class LessonFavouriteAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'created', 'is_active']
    list_filter = ['created', 'user', 'lesson']
    list_editable = ['is_active']


class LessonCompleteAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'user', 'created', 'is_complete']
    list_filter = ['created', 'user']

class VideoAdmin(admin.ModelAdmin):
    list_display = ['filename', 'status', 'orig', 'mp4', 'webm']

admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonHistory, LessonHistoryAdmin)
admin.site.register(LessonFavourite, LessonFavouriteAdmin)
admin.site.register(LessonComplete, LessonCompleteAdmin)
admin.site.register(Video, VideoAdmin)