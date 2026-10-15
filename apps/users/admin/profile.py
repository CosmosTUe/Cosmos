import logging

from django.contrib import admin
from django.http import FileResponse
from django.urls import path

from apps.users.models import Profile
from apps.users.stats import get_date_joined_stats

logger = logging.getLogger(__name__)


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
        # filenames = get_nationality_stats(self.model.objects)  # get file objects of plots
        # TODO you can uncomment above line and comment below line for the button to now show nationality stats
        filenames = get_date_joined_stats(self.model.objects.select_related("user", "institutiontue"))
        response = FileResponse(open(filenames[0], "rb"))

        return response
