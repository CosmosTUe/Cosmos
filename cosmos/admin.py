from django.contrib import admin

from cosmos.models import FileObject, GMM


@admin.register(GMM)
class GMMAdmin(admin.ModelAdmin):
    list_display = ("name", "date")

    search_fields = ["name", "date"]


@admin.register(FileObject)
class FileObjectAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "created_by", "modified", "modified_by", "file", "container"]