from django.contrib import admin

from apps.users.models.user import InstitutionFontys, InstitutionTue


@admin.register(InstitutionTue)
class InstitutionTueAdmin(admin.ModelAdmin):
    list_display = ["username", "department", "program", "tue_id", "card_number", "key_access"]
    list_filter = ["department", "program", "key_access"]


@admin.register(InstitutionFontys)
class InstitutionFontysAdmin(admin.ModelAdmin):
    list_display = ["username", "study"]
    list_filter = ["study"]
