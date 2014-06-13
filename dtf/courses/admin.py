from django.contrib import admin
from lessons.models import Lesson
from courses.models import Course


class LessonInline(admin.TabularInline):
    model = Lesson


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_editable = ['published']
    list_display = ['name', 'published', 'order']

admin.site.register(Course, CourseAdmin)
