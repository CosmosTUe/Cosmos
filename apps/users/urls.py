from django.conf.urls import url
from django.urls import path

from . import views, webhooks

app_name = "cosmos_users"

urlpatterns = [
    path("register/", views.register, name="user_register"),
    path("profile/", views.process_profile_form, name="user_profile"),
    path("delete/", views.delete, name="user_delete"),
    url(r"hook/$", webhooks.sendgrid_webhook, name="email_hook"),
]
