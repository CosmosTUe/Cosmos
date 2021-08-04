from django.contrib import admin

from cosmos.models import GMM, FileObject, Testimonial


@admin.register(GMM)
class GMMAdmin(admin.ModelAdmin):
    list_display = ("name", "date")

    search_fields = ["name", "date"]


@admin.register(FileObject)
class FileObjectAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "created_by", "modified", "modified_by", "file", "container"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["text", "author"]
