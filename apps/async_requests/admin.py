from django.contrib import admin

from apps.async_requests.models import CommandModel

@admin.register(CommandModel)
class CommandModelAdmin(admin.ModelAdmin):
    list_display = ["data"]
