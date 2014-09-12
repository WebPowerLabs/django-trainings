from django.contrib import admin

from .models import Journal, JournalEntry, JournalQuestion


admin.site.register(Journal)
admin.site.register(JournalEntry)
admin.site.register(JournalQuestion)
