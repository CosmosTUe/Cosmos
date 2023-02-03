import logging

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, ButtonHolder, Layout, Submit
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from newsletter.models import Newsletter, Subscription

from apps.async_requests.factory import Factory
from apps.users.forms.error_codes import INVALID_EMAIL, INVALID_EMAIL_CHANGE, INVALID_SUBSCRIBE_TO_EMPTY_EMAIL
from apps.users.helper_functions import (
    is_fontys_email,
    is_tue_email,
    is_valid_institutional_email,
    same_email_institution,
)
from apps.users.models.constants import (
    FONTYS_STUDIES,
    NATIONALITIES,
    NEWSLETTER_RECIPIENTS,
    TUE_DEPARTMENTS,
    TUE_PROGRAMS,
)

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
        profile.save()
        username = self.cleaned_data["username"]
        institution = profile.institution
        if is_tue_email(username):
            institution.department = self.cleaned_data["department"]
            institution.program = self.cleaned_data["program"]
            institution.save()
        elif is_tue_email(username):
            institution.study = self.cleaned_data["study"]
            institution.save()

        if "email" in self.changed_data:
            old_email = self.initial["email"]
            new_email = self.cleaned_data["email"]
            subs = Subscription.objects.filter(email_field=old_email)
            for sub in subs:
                sub.update("unsubscribe")
                new_sub, _ = Subscription.objects.get_or_create(newsletter=sub.newsletter, email_field=new_email)
                new_sub.update("subscribe")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "id-profileUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"
        self.helper.form_tag = False

        username = self.initial.get("username")
        profile = self.instance.profile
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


class PreferencesUpdateForm(forms.Form):
    @staticmethod
    def newsletter_field_name(newsletter):
        return f"newsletter-{newsletter.slug}"

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, initial={}, **kwargs)
        self.user = user
        self.helper = FormHelper(self)
        newsletters = [Newsletter.objects.get(slug__exact="cosmos-news"), Newsletter.objects.get(slug__exact="gmm")]
        recipients = [("NONE", "Disabled")] + NEWSLETTER_RECIPIENTS
        crispy_newsletters = []
        for newsletter in newsletters:
            name = self.newsletter_field_name(newsletter)
            self.fields[name] = forms.ChoiceField(
                label=newsletter.title,
                choices=recipients,
                required=False,
            )
            crispy_newsletters.append(FloatingField(name))

        self.init_newsletter_initials()
        self.set_newsletter_initials(user.username, "TUE")
        self.set_newsletter_initials(user.email, "ALT")

        self.helper.form_id = "id-preferencesUpdateForm"
        self.helper.form_method = "post"
        self.helper.form_action = "cosmos_users:user_profile"
        self.helper.form_tag = False

        self.helper.layout = Layout(HTML('<h3 class="text-white">Email notifications</h3>'), *crispy_newsletters)

        self.helper.add_input(Submit("save_preferences", "Submit"))

    def init_newsletter_initials(self):
        newsletters = Newsletter.objects.all()
        for newsletter in newsletters:
            self.initial[self.newsletter_field_name(newsletter)] = "NONE"

    def set_newsletter_initials(self, email, value):
        subs = Subscription.objects.filter(email_field__exact=email, subscribed=True)
        for sub in subs:
            self.initial[self.newsletter_field_name(sub.newsletter)] = value

    def clean(self):
        if self.user.email == "":
            for sub in self.cleaned_data.values():
                if sub == "ALT":
                    raise ValidationError(
                        "Please set a secondary email, or choose to receive emails at your institution email.",
                        INVALID_SUBSCRIBE_TO_EMPTY_EMAIL,
                    )

        return self.cleaned_data

    def save(self):
        for name, value in self.cleaned_data.items():
            slug = name.lstrip("newsletter-")
            newsletter = Newsletter.objects.get(slug__exact=slug)
            inst_sub, _ = Subscription.objects.get_or_create(newsletter=newsletter, email_field=self.user.username)
            pers_sub, _ = Subscription.objects.get_or_create(newsletter=newsletter, email_field=self.user.email)

            if value == "NONE":
                inst_sub.update("unsubscribe")
                pers_sub.update("unsubscribe")
            elif value == "TUE":
                inst_sub.update("subscribe")
                pers_sub.update("unsubscribe")
            elif value == "ALT":
                inst_sub.update("unsubscribe")
                pers_sub.update("subscribe")
