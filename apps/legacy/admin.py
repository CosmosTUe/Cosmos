from django.contrib import admin

from apps.legacy.models import MysiteProfile
from apps.legacy.tasks import send_migration_emails_task


# Reference used for implementation:
# https://medium.com/@hakibenita/how-to-add-custom-action-buttons-to-django-admin-8d266f5b0d41'
@admin.register(MysiteProfile)
class LegacyProfileAdmin(admin.ModelAdmin):
    """
    Adds extra functionality to the django admin website regarding the sending out of legacy account
    import emails for legacy profiles.
    For more information see:
    https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
    """

    list_display = ["get_username", "department"]
    actions = ["send_migration_email"]

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = "Username"
    get_username.admin_order_field = "user__username"

    def send_migration_email(self, request, queryset):
        send_migration_emails_task.delay([u for u in queryset.values_list("id", flat=True)])
        self.message_user(request, f"{len(queryset)} emails sent!")

    send_migration_email.short_description = "Send migration email"
