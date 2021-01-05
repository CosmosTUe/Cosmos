import logging

from django.contrib import admin
from django.db.models.query import QuerySet

from apps.users.factory import get_newsletter_service
from apps.users.models import Profile

# from apps.users.tasks import sync_newsletter_subcriptions_task

logger = logging.getLogger(__name__)
newsletter_service = get_newsletter_service()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "department", "program", "nationality", "terms_confirmed", "subscribed_newsletter")

    search_fields = ["user__username"]

    actions = ["sync_newsletter_subscriptions"]

    def sync_newsletter_subscriptions(self, request, queryset: QuerySet):
        self.message_user(request, f"Sending {len(queryset)} messages...")
        # breaks with celery, see https://github.com/sendgrid/python-http-client/issues/139
        # sync_newsletter_subscriptions_task.delay([u for u in queryset.values_list("id", flat=True)]).get()
        for u in queryset:
            newsletter_service.update_newsletter_preferences(u, force=True)
        self.message_user(request, f"{len(queryset)} newsletter preferences updated!")
