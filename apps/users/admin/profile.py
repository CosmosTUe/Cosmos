import logging
import os
from zipfile import ZipFile

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import FileResponse
from django.urls import path

from apps.users.factory import get_newsletter_service
from apps.users.models import Profile
from apps.users.stats import get_stats

# from apps.users.tasks import sync_newsletter_subcriptions_task

logger = logging.getLogger(__name__)
newsletter_service = get_newsletter_service()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "department", "program", "nationality", "terms_confirmed", "subscribed_newsletter")

    search_fields = ["user__username"]

    # Used to extend the default admin page to add a button
    change_list_template = "user/admin_add_stats_button.html"

    # Used to extend the get_urls function to add a getstats url
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("getstats/", self.send_stats),
        ]
        return my_urls + urls

    def send_stats(self, request):
        # https://djangosnippets.org/snippets/365/
        filenames = get_stats(self.model.objects)  # get file objects of plots
        zip_path = "/tmp/user-stats.zip"
        if os.path.exists(zip_path):
            os.remove(zip_path)
        zip_obj = ZipFile(zip_path, "w")
        for files in filenames:
            zip_obj.write(files, os.path.basename(files))
            os.remove(files)
        zip_obj.close()
        response = FileResponse(open(zip_path, "rb"))

        return response

    actions = ["sync_newsletter_subscriptions"]

    def sync_newsletter_subscriptions(self, request, queryset: QuerySet):
        self.message_user(request, f"Sending {len(queryset)} messages...")
        # breaks with celery, see https://github.com/sendgrid/python-http-client/issues/139
        # sync_newsletter_subscriptions_task.delay([u for u in queryset.values_list("id", flat=True)]).get()
        for u in queryset:
            newsletter_service.update_newsletter_preferences(u, force=True)
        self.message_user(request, f"{len(queryset)} newsletter preferences updated!")
