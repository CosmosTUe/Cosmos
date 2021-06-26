from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, HTML, Layout
from crispy_bootstrap5.bootstrap5 import FloatingField
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm


class CosmosLoginForm(AuthenticationForm):
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


class CosmosSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tage = False
        self.helper.layout = Layout(FloatingField())
