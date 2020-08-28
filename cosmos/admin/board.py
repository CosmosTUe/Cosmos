from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from cosmos.models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ("name", "description", "period_from", "period_to")

    search_fields = ["user__username"]
