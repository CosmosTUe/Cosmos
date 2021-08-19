import logging

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.async_requests.commands import SubscribeCommand, UnsubscribeCommand
from apps.async_requests.factory import Factory
from apps.users.forms.errors import INVALID_EMAIL, INVALID_EMAIL_CHANGE, INVALID_SUBSCRIBE_TO_EMPTY_EMAIL
from apps.users.helper_functions import (
    is_fontys_email,
    is_tue_email,
    is_valid_institutional_email,
    same_email_institution,
)
from apps.users.models.user import Profile
from apps.users.models.user.constants import FONTYS_STUDIES, NATIONALITIES, TUE_DEPARTMENTS, TUE_PROGRAMS
from apps.users.models.user.institution import InstitutionFontys, InstitutionTue

logger = logging.getLogger(__name__)
executor = Factory.get_executor()


class ProfileUpdateForm(forms.ModelForm):
    username = forms.EmailField(max_length=254, label="Institution email")
    email = forms.EmailField(max_length=254, label="Personal email (optional)", required=False)
    nationality = forms.ChoiceField(choices=list(zip(NATIONALITIES, NATIONALITIES)))

    # When the user is from TUe, 'study' is empty.
    # When the user is from Fontys, 'department' and 'program' is empty.
    # In order for the form to be valid, fields from Institution classes has 'required' set to False.

    # Tue:
    department = forms.ChoiceField(required=False, choices=list(zip(TUE_DEPARTMENTS, TUE_DEPARTMENTS)))
    program = forms.ChoiceField(required=False, choices=list(zip(TUE_PROGRAMS, TUE_PROGRAMS)))

    # Fontys:
    study = forms.ChoiceField(required=False, choices=list(zip(FONTYS_STUDIES, FONTYS_STUDIES)))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not is_valid_institutional_email(data):
            raise ValidationError("Please enter your institutional email.", INVALID_EMAIL)

        current_username = self.instance.username
        if not same_email_institution(data, current_username):
            raise ValidationError(
                "Invalid operation. Please contact the website admins to change profile institution.",
                INVALID_EMAIL_CHANGE,
            )
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

        if "email" in self.changed_data and profile.subscribed_newsletter and profile.newsletter_recipient == "ALT":
            old_email = self.initial["email"]
            executor.add_command(UnsubscribeCommand(old_email))
            new_email = self.cleaned_data["email"]
            executor.add_command(SubscribeCommand(new_email, profile.user.first_name, profile.user.last_name))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"
        self.helper.form_tag = False

        username = self.initial.get("username")
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        self.initial["nationality"] = profile.nationality
        if is_tue_email(username):
            hidden_tue = ""
            hidden_fontys = "hidden"
            self.initial["department"] = profile.institution.department
            self.initial["program"] = profile.institution.program
        elif is_fontys_email(username):
            hidden_tue = "hidden"
            hidden_fontys = ""
            self.initial["study"] = profile.institution.study
        else:
            hidden_tue = ""
            hidden_fontys = ""

        self.helper.layout = Layout(
            FloatingField("first_name"),
            FloatingField("last_name"),
            FloatingField("username"),
            FloatingField("email"),
            FloatingField("nationality"),
            FloatingField("department", type=hidden_tue),
            FloatingField("program", type=hidden_tue),
            FloatingField("study", type=hidden_fontys),
            ButtonHolder(Submit("save_profile", "Submit")),
        )


class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-passwordUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            FloatingField("old_password"),
            FloatingField("new_password1"),
            FloatingField("new_password2"),
        )

        self.helper.add_input(Submit("save_password", "Submit"))


class PreferencesUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["subscribed_newsletter", "newsletter_recipient"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-preferencesUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Field("subscribed_newsletter"),
            Field("newsletter_recipient"),
        )

        self.helper.add_input(Submit("save_preferences", "Submit"))

    def clean(self):
        if (
            self.instance.user.email == ""
            and self.cleaned_data["newsletter_recipient"]
            and self.cleaned_data["subscribed_newsletter"]
        ):
            raise ValidationError(
                "Please set a secondary email or choose to receive the newsletters at your institution email.",
                INVALID_SUBSCRIBE_TO_EMPTY_EMAIL,
            )
        return self.cleaned_data

    def save(self, commit=True):
        old_newsletter_state = self.initial["subscribed_newsletter"]
        old_newsletter_recipient = self.initial["newsletter_recipient"]

        newsletter_service = Factory.get_newsletter_service()
        newsletter_service.update_newsletter_preferences(self.instance, old_newsletter_state, old_newsletter_recipient)
        return super(PreferencesUpdateForm, self).save(commit)


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
        self.helper.form_tag = False

        self.helper.layout = Layout(
            FloatingField("tue_id"),
            FloatingField("card_number"),
        )

        self.helper.add_input(Submit("save_key_access", "Submit"))
