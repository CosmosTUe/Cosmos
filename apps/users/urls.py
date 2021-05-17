from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views, webhooks

app_name = "cosmos_users"

urlpatterns = [
    path("profile/", views.profile, name="user_profile"),
    # path("delete/", views.delete, name="user_delete"),
    path(
        "register/",
        views.RegistrationWizard.as_view(views.FORMS, condition_dict=views.CONDITION_DICT),
        name="user_register",
    ),
    path("register/done/", views.registration_done, name="registration_done"),
    path("confirm/<uidb64>/<token>/", views.activate, name="confirm_registration"),
    path("committee/", views.committee_overview, name="committee_overview"),
    path("committee/<slug>/", views.committee_subpage, name="committee_subpage"),
    url(r"hook/$", csrf_exempt(webhooks.SendGridWebhook.as_view()), name="email_hook"),
]
