# import re

# from cms.utils.compat.forms import UserChangeForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.users.models.user.constants import FONTYS_STUDIES, NATIONALITIES, TUE_DEPARTMENTS, TUE_PROGRAMS
from apps.users.models.user.institution import InstitutionFontys, InstitutionTue
from apps.users.models.user.profile import Profile


class ProfileUpdateForm(forms.ModelForm):

    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
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
        if (
            not data.endswith("@student.tue.nl")
            or not data.endswith("@alumni.tue.nl")
            or not data.endswith("@fontys.nl")
        ):
            raise ValidationError("Please enter your institutional email.")
        return data

    def save(self, commit=True):
        instance = super().save(commit=True)
        profile = instance.profile
        profile.nationality = self.cleaned_data["nationality"]
        if self.cleaned_data["username"].endswith("tue.nl"):
            institution = InstitutionTue.objects.get(profile=profile)
            institution.department = self.cleaned_data["department"]
            institution.program = self.cleaned_data["program"]
        elif self.cleaned_data["username"].endswith("fontys.nl"):
            institution = InstitutionFontys.objects.get(profile=profile)
            institution.study = self.cleaned_data["study"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"

        self.helper.add_input(Submit("submit", "Submit"))


class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-passwordUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"

        self.helper.add_input(Submit("submit", "Submit"))


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

        self.helper.add_input(Submit("submit", "Submit"))


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

        self.helper.add_input(Submit("submit", "Submit"))


# class MemberCreateForm(UserCreationForm):
#     """
#     A form that creates a user for a COSMOS member, with a given TU/e email. Makes use built-in User model of Django:
#     stores first name, last name, TU/e email (saved as username in the database), email (personal email) and password.

#     Extra fields are defined in ProfileCreateForm.
#     """

#     first_name = forms.CharField(max_length=30, required=True, initial="")
#     last_name = forms.CharField(max_length=30, required=True, initial="")
#     username = forms.EmailField(
#         max_length=254,
#         label="TU/e email",
#         help_text="Required. Inform a valid TU/e email address.",
#         required=True,
#         initial="",
#     )
#     email = forms.EmailField(
#         max_length=254,
#         label="Personal email",
#         required=False,
#         help_text="Optional. Inform a valid email address.",
#         initial="",
#     )

#     error_css_class = "is-invalid"
#     required_css_class = "required"

#     class Meta:
#         model = User
#         fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         # When registering check if user already exists
#         if User.objects.filter(username=username).exists():
#             raise ValidationError(
#                 "There is already a user with this email in our system, please try with a different one.",
#                 code="duplicate_user",
#             )
#         if not re.search("([@.])tue.nl$", username):
#             # Ensures email is from TUe (endswith ".tue.nl" or "@tue.nl"
#             raise ValidationError("This field must be a valid TU/e email address", code="nontue_email")
#         # Cleaning requires a return
#         return username

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["password1"].initial = ""
#         self.fields["password2"].initial = ""


# class MemberUpdateForm(UserChangeForm):
#     """
#     A form that allows a user to update their personal information inside of the User model of Django. This includes:
#     first name, last name, TU/e email (username in the database), and email (personal email)

#     Extra fields are defined in ProfileUpdateForm.
#     """

#     username = forms.EmailField(
#         max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
#     )
#     email = forms.EmailField(
#         max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
#     )

#     class Meta:
#         model = User
#         fields = ["first_name", "last_name", "username", "email"]

#     def clean_username(self):
#         username = self.cleaned_data.get("username")
#         # When updating, only check if email valid
#         if not re.search("([@.])tue.nl$", username):
#             # Ensures email is from TUe (endswith ".tue.nl" or "@tue.nl"
#             raise ValidationError("This field must be a valid TU/e email address", code="nontue_email")
#         # Cleaning requires a return
#         return username


# class ProfileCreateForm(forms.ModelForm):
#     """
#     A form that creates additional information about a COSMOS member.
#     """

#     terms_confirmed = forms.BooleanField(initial=False, required=True)
#     subscribed_newsletter = forms.BooleanField(label="Receive newsletter via email", initial=False, required=False)

#     class Meta:
#         model = Profile
#         fields = ["nationality", "department", "program", "subscribed_newsletter", "terms_confirmed"]

#     error_css_class = "error"
#     required_css_class = "required"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["nationality"].choices = [("", "Please select your nationality")] + list(
#             self.fields["nationality"].choices
#         )[1:]
#         self.fields["department"].choices = [("", "Please select your department")] + list(
#             self.fields["department"].choices
#         )[1:]
#         self.fields["program"].choices = [("", "Please select your program")] + list(self.fields["program"].choices)[1:]


# class ProfileUpdateForm(forms.ModelForm):
#     """
#     A form that modifies additional information about a COSMOS member.
#     """

#     class Meta:
#         model = Profile
#         fields = ["nationality", "department", "program", "tue_id", "card_number", "subscribed_newsletter"]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["nationality"].choices = [("", "Please select your nationality")] + list(
#             self.fields["nationality"].choices
#         )[1:]
#         self.fields["department"].choices = [("", "Please select your department")] + list(
#             self.fields["department"].choices
#         )[1:]
#         self.fields["program"].choices = [("", "Please select your program")] + list(self.fields["program"].choices)[1:]
