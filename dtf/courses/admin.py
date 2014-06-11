from django.contrib import admin
from lessons.models import Lesson
from courses.models import Course


class LessonInline(admin.TabularInline):
    model = Course


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_editable = ['published']
    list_display = ['name', 'published']

admin.site.register(Course, CourseAdmin)
