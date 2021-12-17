import os
from zipfile import ZipFile

from django.contrib import admin
from django.http import FileResponse
from django.urls import path

from apps.users.models.institution import InstitutionFontys, InstitutionTue
from apps.users.stats import get_major_stats


@admin.register(InstitutionTue)
class InstitutionTueAdmin(admin.ModelAdmin):
    list_display = ["username", "department", "program"]
    list_filter = ["department", "program"]
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
        # https://djangosnippets.org/snippets/364/
        filenames = get_major_stats(self.model.objects)  # get file objects of plots
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


@admin.register(InstitutionFontys)
class InstitutionFontysAdmin(admin.ModelAdmin):
    list_display = ["username", "study"]
    list_filter = ["study"]
