from django.contrib import admin
from lessons.models import Lesson
from courses.models import Course, CourseHistory, CourseFavourite


class LessonInline(admin.TabularInline):
    model = Lesson


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_editable = ['published']
    list_display = ['name', 'published', 'order']


class CourseHistoryAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'created']
    list_filter = ['created']


class CourseFavouriteAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'created']
    list_filter = ['created']

admin.site.register(Course, CourseAdmin)
admin.site.register(CourseHistory, CourseHistoryAdmin)
admin.site.register(CourseFavourite, CourseFavouriteAdmin)
