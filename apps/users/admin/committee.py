from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from apps.users.models import Committee


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ("name", "description", "hidden")
    list_filter = ("hidden",)

    search_fields = ["user__username"]
