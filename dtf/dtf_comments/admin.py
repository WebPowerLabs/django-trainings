from django.contrib import admin
from dtf_comments.models import DTFComment


class DTFCommentAdmin(admin.ModelAdmin):

    def flag(self, obj):
        flag_name = ''
        try:
            flag_name = obj.flags.values()[0]['flag']
        except IndexError:
            pass
        return flag_name

    list_display = ['name', 'content_type', 'object_pk', 'site', 'ip_address',
                    'submit_date', 'flag', 'is_public', 'is_removed']
    list_filter = ['submit_date', 'site', 'is_public', 'is_removed',
                   'flags__flag']

admin.site.register(DTFComment, DTFCommentAdmin)
