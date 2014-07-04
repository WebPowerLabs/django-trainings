from django.contrib import admin
from dtf_comments.models import DTFComment


class DTFCommentAdmin(admin.ModelAdmin):
    list_filter = ['submit_date']
    list_display = ['user_name', 'site', 'ip_address', 'submit_date',
                    'is_public', 'is_removed']

admin.site.register(DTFComment, DTFCommentAdmin)
