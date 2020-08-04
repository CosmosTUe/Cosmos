import re

from cms.utils.compat.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from cosmos.models.user import Profile


class MemberCreateForm(UserCreationForm):
    """
    A form that creates a user for a COSMOS member, with a given TU/e email. Makes use built-in User model of Django:
    stores first name, last name, TU/e email (saved as username in the database), email (personal email) and password.

    Extra fields are defined in ProfileCreateForm.
    """

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # When registering check if user already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "There is already a user with this email in our system, please try with a different one.",
                code="duplicate_user",
            )
        if not re.search("([@.])tue.nl$", username):
            # Ensures email is from TUe (endswith ".tue.nl" or "@tue.nl"
            raise ValidationError("This field must be a valid TU/e email address", code="nontue_email")
        # Cleaning requires a return
        return username


class MemberUpdateForm(UserChangeForm):
    """
    A form that allows a user to update their personal information inside of the User model of Django. This includes:
    first name, last name, TU/e email (username in the database), and email (personal email)

    Extra fields are defined in ProfileUpdateForm.
    """

    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # When updating, only check if email valid
        if not re.search("([@.])tue.nl$", username):
            # Ensures email is from TUe (endswith ".tue.nl" or "@tue.nl"
            raise ValidationError("This field must be a valid TU/e email address", code="nontue_email")
        # Cleaning requires a return
        return username


class ProfileCreateForm(forms.ModelForm):
    """
    A form that creates additional information about a COSMOS member.
    """

    class Meta:
        model = Profile
        fields = ["nationality", "department", "program"]


class ProfileUpdateForm(ProfileCreateForm):
    """
    A form that modifies additional information about a COSMOS member.
    """

    class Meta:
        model = Profile
        fields = [
            "nationality",
            "department",
            "program",
            "tue_id",
            "card_number",
            "status",
            "key_access",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["status"].disabled = True
        self.fields["key_access"].disabled = True
