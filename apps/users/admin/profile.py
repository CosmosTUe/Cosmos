import logging
import os
from zipfile import ZipFile

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import FileResponse
from django.urls import path

from apps.async_requests.factory import Factory
from apps.users.models import Profile
from apps.users.stats import get_stats

# from apps.users.tasks import sync_newsletter_subcriptions_task

logger = logging.getLogger(__name__)
executor = Factory.get_executor()
newsletter_service = Factory.get_newsletter_service()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "nationality", "terms_confirmed", "subscribed_newsletter")

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
        for profile in queryset:
            newsletter_service.sync_newsletter_preferences(profile)
        executor.execute()
        self.message_user(request, f"{len(queryset)} newsletter preferences updated!")
