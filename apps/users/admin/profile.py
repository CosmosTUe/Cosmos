import os
from zipfile import ZipFile

from django.contrib import admin
from django.http import HttpResponse, FileResponse
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
        # response = HttpResponse(open(zip_path).read(), content_type="application/zip")
        # response["Content-Disposition"] = "attachment; filename=%s" % os.path.basename(zip_path)
        response = FileResponse(open(zip_path, "rb"))

        return response
