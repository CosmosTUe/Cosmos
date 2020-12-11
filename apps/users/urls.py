from django.urls import path

from . import views

app_name = "cosmos_users"

urlpatterns = [
    # path("register/", views.register, name="user_register"),
    # path("profile/", views.profile, name="user_profile"),
    # path("delete/", views.delete, name="user_delete"),
    path(
        "register/",
        views.RegistrationWizard.as_view(views.FORMS, condition_dict=views.CONDITION_DICT),
        name="registration",
    ),
    path("register/done/", views.registration_done, name="registration_done"),
    path("confirm/<uidb64>/<token>/", views.activate, name="confirm_registration"),
]
