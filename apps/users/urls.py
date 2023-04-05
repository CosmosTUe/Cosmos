from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls.base import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from . import views, webhooks
from .forms.authorization import CosmosPasswordChangeForm, CosmosPasswordResetForm, CosmosSetPasswordForm

app_name = "cosmos_users"

urlpatterns = [
    # auth urls
    path("login/", views.CosmosLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            form_class=CosmosPasswordChangeForm, success_url=reverse_lazy("cosmos_users:password_change_done")
        ),
        name="password_change",
    ),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            form_class=CosmosPasswordResetForm, success_url=reverse_lazy("cosmos_users:password_reset_done")
        ),
        name="password_reset",
    ),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class=CosmosSetPasswordForm, success_url=reverse_lazy("cosmos_users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # custom urls
    path("profile/", views.profile, name="user_profile"),
    path("delete/", views.delete, name="user_delete"),
    path(
        "register/",
        views.RegistrationWizard.as_view(views.FORMS, condition_dict=views.CONDITION_DICT),
        name="user_register",
    ),
    path("register/done/", views.registration_done, name="registration_done"),
    path("confirm/<uidb64>/<token>/", views.activate, name="confirm_registration"),
    path("hook/", csrf_exempt(webhooks.SendGridWebhook.as_view()), name="email_hook"),
    path("reconfirm/", views.ReconfirmView.as_view(), name="reconfirm"),
    path("reconfirm_done/", views.reconfirm_done, name="reconfirm-done"),
    path("profile#<active_tab>", views.profile, name="subscribe-newsletter"),
]
