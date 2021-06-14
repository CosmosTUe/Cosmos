from django.contrib import admin

from apps.users.models import Committee


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

    search_fields = ["user__username"]
