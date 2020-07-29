from django.contrib import admin

from cosmos.models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "period_from", "period_to")

    search_fields = ["user__username"]
