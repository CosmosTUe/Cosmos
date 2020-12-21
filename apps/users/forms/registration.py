from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.users.models.user.constants import NATIONALITIES
from apps.users.models.user.institution import InstitutionFontys, InstitutionTue
from apps.users.models.user.profile import Profile


class RegisterUserForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, initial="")
    last_name = forms.CharField(max_length=30, required=True, initial="")
    username = forms.EmailField(
        max_length=254,
        label="Institutional Email",
        help_text="Required. Please fill in your institutional email address.",
        required=True,
        initial="",
    )
    email = forms.EmailField(
        max_length=254,
        label="Personal email",
        required=False,
        help_text="Optional, Please fill in a valid email address.",
        initial="",
    )
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, initial="")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, initial="")

    # profile fields
    nationality = forms.ChoiceField(choices=list(zip(NATIONALITIES, NATIONALITIES)))
    terms_confirmed = forms.BooleanField()
    subscribed_newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def clean_nationality(self):
        data = self.cleaned_data["nationality"]
        if data not in NATIONALITIES:
            raise ValidationError("Please enter your nationality.")
        return data

    def clean_username(self):
        data = self.cleaned_data["username"]
        if not data.endswith("@student.tue.nl") or not data.endswith("@alumni.tue.nl") or not data.endswith("@fontys.nl"):
            raise ValidationError("Please enter your institutional email.")
        return data

    def save(self, commit=True):
        instance = super().save(commit=True)
        profile = Profile(
            user=instance,
            nationality=self.cleaned_data["nationality"],
            terms_confirmed=self.cleaned_data["terms_confirmed"],
            subscribed_newsletter=self.cleaned_data["subscribed_newsletter"],
        )
        profile.save()
        return instance


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["nationality", "terms_confirmed", "subscribed_newsletter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["nationality"].choices = [("", "Please select your nationality")] + list(
            self.fields["nationality"].choices
        )[1:]


class RegisterTueForm(forms.ModelForm):
    class Meta:
        model = InstitutionTue
        fields = ["department", "program"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].choices = [("", "Please select your department")] + list(
            self.fields["department"].choices
        )[1:]
        self.fields["program"].choices = [("", "Please select your program")] + list(self.fields["program"].choices)[1:]


class RegisterFontysForm(forms.ModelForm):
    class Meta:
        model = InstitutionFontys
        fields = ["study"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["study"].choices = [("", "Please select your study")] + list(
            self.fields["study"].choices
        )[1:]
