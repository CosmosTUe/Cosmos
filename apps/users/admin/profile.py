from django.contrib import admin
from django.db.models.query import QuerySet

from apps.users.factory import get_newsletter_service
from apps.users.models import Profile

newsletter_service = get_newsletter_service()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "key_access")

    search_fields = ["user__username"]

    actions = ["sync_newsletter_subscriptions"]

    def sync_newsletter_subscriptions(self, request, queryset: QuerySet):
        # TODO hey Bart pls convert to celery shared_task alsjeblieft
        for profile in queryset:
            newsletter_service.update_newsletter_preferences(profile)
        self.message_user(request, f"{len(queryset)} newsletter preferences updated!")
