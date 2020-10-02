from django.urls import path

from . import views

app_name = "cosmos_users"

urlpatterns = [
    path("accounts/register/", views.register, name="user_register"),
    path("accounts/profile/", views.profile, name="user_profile"),
    path("accounts/delete", views.delete, name="user_delete"),
]
