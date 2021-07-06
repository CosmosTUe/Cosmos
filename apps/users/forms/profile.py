import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.async_requests.factory import Factory
from apps.users.helper_functions import is_fontys_email, is_tue_email, is_valid_institutional_email
from apps.users.models.user import Profile
from apps.users.models.user.constants import FONTYS_STUDIES, NATIONALITIES, TUE_DEPARTMENTS, TUE_PROGRAMS
from apps.users.models.user.institution import InstitutionFontys, InstitutionTue

logger = logging.getLogger(__name__)
newsletter_service = Factory.get_newsletter_service()


class ProfileUpdateForm(forms.ModelForm):

    username = forms.EmailField(
        max_length=254, label="Institution email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )
    nationality = forms.ChoiceField(choices=list(zip(NATIONALITIES, NATIONALITIES)))

    # Tue:
    department = forms.ChoiceField(choices=list(zip(TUE_DEPARTMENTS, TUE_DEPARTMENTS)))
    program = forms.ChoiceField(choices=list(zip(TUE_PROGRAMS, TUE_PROGRAMS)))

    # Fontys:
    study = forms.ChoiceField(choices=list(zip(FONTYS_STUDIES, FONTYS_STUDIES)))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not is_valid_institutional_email(data):
            raise ValidationError("Please enter your institutional email.")
        return data

    def save(self, commit=True):
        instance = super().save(commit=True)
        profile = instance.profile
        profile.nationality = self.cleaned_data["nationality"]
        username = self.cleaned_data["username"]
        if is_tue_email(username):
            institution = InstitutionTue.objects.get(profile=profile)
            institution.department = self.cleaned_data["department"]
            institution.program = self.cleaned_data["program"]
        elif is_tue_email(username):
            institution = InstitutionFontys.objects.get(profile=profile)
            institution.study = self.cleaned_data["study"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"

        username = self.initial.get("username")
        if is_tue_email(username):
            hidden_tue = ""
            hidden_fontys = "hidden"
        elif is_fontys_email(username):
            hidden_tue = "hidden"
            hidden_fontys = ""
        else:
            hidden_tue = ""
            hidden_fontys = ""

        self.helper.layout = Layout(
            Field("first_name"),
            Field("last_name"),
            Field("username"),
            Field("email"),
            Field("nationality"),
            Field("department", type=hidden_tue),
            Field("program", type=hidden_tue),
            Field("study", type=hidden_fontys),
            ButtonHolder(Submit("save_profile", "Submit")),
        )


class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-passwordUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"

        self.helper.add_input(Submit("save_password", "Submit"))


class PreferencesUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["subscribed_newsletter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-preferencesUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"

        self.helper.add_input(Submit("save_preferences", "Submit"))


class KeyAccessUpdateForm(forms.ModelForm):
    class Meta:
        model = InstitutionTue
        fields = ["tue_id", "card_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-keyAccessUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"

        self.helper.add_input(Submit("save_key_access", "Submit"))
