from django.contrib import admin
from django.core import mail

from apps.legacy.mail import create_legacy_account_email
from apps.legacy.models import MysiteProfile


@admin.register(MysiteProfile)
# TODO reference
# https://medium.com/@hakibenita/how-to-add-custom-action-buttons-to-django-admin-8d266f5b0d41
class LegacyProfileAdmin(admin.ModelAdmin):
    list_display = ["get_username", "department"]
    actions = ["send_migration_email"]

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "Username"
    get_username.admin_order_field = "user__username"

    def send_migration_email(self, request, queryset):
        emails = []
        for profile in queryset:
            emails.append(create_legacy_account_email(profile))
        connection = mail.get_connection()
        connection.send_messages(emails)
        self.message_user(request, f"{len(queryset)} emails sent!")

    send_migration_email.short_description = "Send migration email"
