from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from newsletter.models import Newsletter, Subscription

from apps.users.forms.error_codes import INVALID_EMAIL
from apps.users.helper_functions import is_valid_institutional_email
from apps.users.models.constants import NATIONALITIES
from apps.users.models.institution import InstitutionFontys, InstitutionTue
from apps.users.models.profile import Profile


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, initial="", widget=forms.TextInput(attrs={"autofocus": True})
    )
    last_name = forms.CharField(max_length=30, required=True, initial="")
    username = forms.EmailField(
        max_length=254,
        label="Institutional Email",
        required=True,
        initial="",
    )
    email = forms.EmailField(
        max_length=254,
        label="Personal email (optional)",
        required=False,
        initial="",
    )
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password", required=True, initial="")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Password confirmation", required=True, initial="")

    # profile fields
    nationality = forms.ChoiceField(choices=list(zip(NATIONALITIES, NATIONALITIES)))
    terms_confirmed = forms.BooleanField()

    # newsletters
    newsletter_cosmos_news = forms.BooleanField(label="Subscribe to the COSMOS newsletter", required=False)
    newsletter_gmm = forms.BooleanField(label="Subscribe to GMM Invites", required=False)

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
        if not is_valid_institutional_email(data):
            raise ValidationError("Please enter your institutional email.", INVALID_EMAIL)
        return data

    def save(self, commit=True):
        instance = super().save(commit=True)
        profile = Profile(
            user=instance,
            nationality=self.cleaned_data["nationality"],
            terms_confirmed=self.cleaned_data["terms_confirmed"],
        )
        profile.save()

        newsletter_preferences = [
            (Newsletter.objects.get(slug__exact="cosmos-news"), self.cleaned_data["newsletter_cosmos_news"]),
            (Newsletter.objects.get(slug__exact="gmm"), self.cleaned_data["newsletter_gmm"]),
        ]
        # create unactivated subscription objects using institutional email
        for (newsletter, preference) in newsletter_preferences:
            if preference:
                Subscription.objects.create(newsletter=newsletter, email_field=instance.username)

        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_register"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("first_name"),
            FloatingField("last_name"),
            FloatingField("username"),
            FloatingField("email"),
            FloatingField("password1"),
            FloatingField("password2"),
            FloatingField("nationality"),
            Field("terms_confirmed"),
            Field("newsletter_cosmos_news"),
            Field("newsletter_gmm"),
        )


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
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_register"
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("department"),
            FloatingField("program"),
        )

        # self.helper.add_input(Button("wizard_goto_step", "0"))
        # self.helper.add_input(Submit("submit", "Submit"))


class RegisterFontysForm(forms.ModelForm):
    class Meta:
        model = InstitutionFontys
        fields = ["study"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["study"].choices = [("", "Please select your study")] + list(self.fields["study"].choices)[1:]
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_register"
        self.helper.form_tag = False
        self.helper.layout = Layout(FloatingField("study"))

        # self.helper.add_input(Button("wizard_goto_step", "0"))
        # self.helper.add_input(Submit("submit", "Submit"))


class ReconfirmationForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        label="Institutional email",
        required=True,
        initial="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(FloatingField("email"))
        self.helper.form_tag = False