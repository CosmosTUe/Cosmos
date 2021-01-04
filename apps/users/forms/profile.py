import re

from cms.utils.compat.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.users.factory import get_newsletter_service
from apps.users.models.user import Profile
from apps.users.models.user.constants import DEPARTMENTS, NATIONALITIES, NEWSLETTER_RECIPIENTS, PROGRAMS

newsletter_service = get_newsletter_service()


class MemberCreateForm(UserCreationForm):
    """
    A form that creates a user for a COSMOS member, with a given TU/e email. Makes use built-in User model of Django:
    stores first name, last name, TU/e email (saved as username in the database), email (personal email) and password.

    Extra fields are defined in ProfileCreateForm.
    """

    first_name = forms.CharField(max_length=30, required=True, initial="")
    last_name = forms.CharField(max_length=30, required=True, initial="")
    username = forms.EmailField(
        max_length=254,
        label="TU/e email",
        help_text="Required. Inform a valid TU/e email address.",
        required=True,
        initial="",
    )
    email = forms.EmailField(
        max_length=254,
        label="Personal email",
        required=False,
        help_text="Optional. Inform a valid email address.",
        initial="",
    )

    error_css_class = "is-invalid"
    required_css_class = "required"

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].initial = ""
        self.fields["password2"].initial = ""


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

    terms_confirmed = forms.BooleanField(initial=False, required=True)
    subscribed_newsletter = forms.BooleanField(label="Receive newsletter via email", initial=False, required=False)
    newsletter_recipient = forms.ChoiceField(
        label="Newsletter subscription email", initial="TUE", required=True, choices=NEWSLETTER_RECIPIENTS
    )

    class Meta:
        model = Profile
        fields = [
            "nationality",
            "department",
            "program",
            "subscribed_newsletter",
            "newsletter_recipient",
            "terms_confirmed",
        ]

    error_css_class = "error"
    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nationality"].choices = [("", "Please select your nationality")] + list(
            self.fields["nationality"].choices
        )[1:]
        self.fields["department"].choices = [("", "Please select your department")] + list(
            self.fields["department"].choices
        )[1:]
        self.fields["program"].choices = [("", "Please select your program")] + list(self.fields["program"].choices)[1:]

    def save(self, *args, **kwargs):
        obj: Profile = super().save(*args, **kwargs)
        if obj.has_changed():
            newsletter_service.update_newsletter_preferences(obj)
        obj.update_states()
        return self.instance


class ProfileUpdateForm(forms.ModelForm):
    """
    A form that modifies additional information about a COSMOS member.
    """

    nationality = forms.ChoiceField(required=False, choices=list(zip(NATIONALITIES, NATIONALITIES)))
    department = forms.ChoiceField(required=False, choices=list(zip(DEPARTMENTS, DEPARTMENTS)))
    program = forms.ChoiceField(required=False, choices=list(zip(PROGRAMS, PROGRAMS)))
    newsletter_recipient = forms.ChoiceField(
        required=False, choices=list(zip(NEWSLETTER_RECIPIENTS, NEWSLETTER_RECIPIENTS))
    )

    class Meta:
        model = Profile
        fields = [
            "nationality",
            "department",
            "program",
            "tue_id",
            "card_number",
            "subscribed_newsletter",
            "newsletter_recipient",
        ]

    def save(self, *args, **kwargs):
        obj: Profile = super().save(*args, **kwargs)
        if obj.has_changed():
            newsletter_service.update_newsletter_preferences(obj)
        obj.update_states()
        return self.instance
