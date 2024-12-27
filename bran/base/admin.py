from django.contrib import admin

from bran.base.models import SendEmail


class SendEmailAdmin(admin.ModelAdmin):
    list_display = ('created', 'email_from', 'subject')
    search_fields = ('email_from', 'subject', 'message')
    list_filter = ('created',)


admin.site.register(SendEmail, SendEmailAdmin)
