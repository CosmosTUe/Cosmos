from django.contrib import admin
from django.urls import path

from apps.users.models import Profile
from apps.users.stats import get_stats


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "key_access")

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
        get_stats(Profile.objects)
