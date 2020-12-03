from django.contrib import admin
from django.urls import path


from apps.users.models.user.profile import Profile
from stats import getStats

# https://docs.djangoproject.com/en/3.1/topics/db/aggregation/
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/
# https://hakibenita.com/how-to-add-custom-action-buttons-to-django-admin
# https://dev.to/leondaz/how-to-execute-code-from-admin-page-in-django-229b#naive-implementation
# https://books.agiliq.com/projects/django-admin-cookbook/en/latest/action_buttons.html


@admin.register(Profile)
class UserStats(admin.ModelAdmin):

    change_list_template = "templates/admin_add_stats_button.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("getstats/", self.send_stats),
        ]
        return my_urls + urls

    def send_stats(self, request):
        getStats(Profile.objects)
