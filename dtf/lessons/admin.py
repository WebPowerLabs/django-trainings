from django.contrib import admin
from lessons.models import Lesson
from resources.models import Resource


class ResourceInLine(admin.TabularInline):
    model = Resource


class LessonAdmin(admin.ModelAdmin):
    inlines = [ResourceInLine]
    list_filter = ['course']
    list_editable = ['published']
    list_display = ['name', 'published', '_order']

admin.site.register(Lesson, LessonAdmin)




