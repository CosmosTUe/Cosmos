import logging
import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.users.factory import get_newsletter_service
from apps.users.models.user import Profile
from apps.users.models.user.constants import DEPARTMENTS, NATIONALITIES, NEWSLETTER_RECIPIENTS, PROGRAMS

logger = logging.getLogger(__name__)
newsletter_service = get_newsletter_service()


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
    newsletter_recipient = forms.ChoiceField(required=False, choices=NEWSLETTER_RECIPIENTS)

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
