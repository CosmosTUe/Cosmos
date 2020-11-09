from django.contrib import admin

from apps.users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "key_access")

    search_fields = ["user__username"]
