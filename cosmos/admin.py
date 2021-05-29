from django.contrib import admin

from cosmos.models import GMM


@admin.register(GMM)
class GMMAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "slides", "minutes")

    search_fields = ["name", "date"]
