from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UsernameField,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.safestring import SafeString

from apps.users.forms.error_codes import INVALID_EMAIL
from apps.users.helper_functions import is_valid_institutional_email


class CosmosLoginForm(AuthenticationForm):
    username = UsernameField(label="Institutional Email", widget=forms.TextInput(attrs={"autofocus": True}))
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("username"),
            FloatingField("password"),
            Div(
                Field("remember_me"),
                HTML("""<a href="{% url 'cosmos_users:password_reset' %}" class="ms-auto">Forgot your password?</a>"""),
                css_class="d-flex",
            ),
        )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                SafeString(
                    f"""This has not been activated, click <a href='{reverse("cosmos_users:reconfirm")}'>here</a>
                     to resend the activation email."""
                ),
                code="inactive",
            )
        return super().confirm_login_allowed(user)

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not is_valid_institutional_email(data):
            raise ValidationError("Please use your institutional email to login.", INVALID_EMAIL)

        return data


class CosmosPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("old_password"),
            FloatingField("new_password1"),
            FloatingField("new_password2"),
        )


class CosmosPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(FloatingField("email"))

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        # derived form super class
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        # modified
        email = self.cleaned_data["email"]
        users = User.objects.filter(**{"username__iexact": email, "is_active": True})
        if len(users) == 0:
            return
        user = users[0]

        context = {
            "email": user.username,
            "domain": domain,
            "site_name": site_name,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": token_generator.make_token(user),
            "protocol": "https" if use_https else "http",
            **(extra_email_context or {}),
        }
        self.send_mail(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            user.username,
            html_email_template_name=html_email_template_name,
        )


class CosmosSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(FloatingField())
