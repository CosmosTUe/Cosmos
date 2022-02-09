from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.exceptions import ValidationError

from apps.events.errors import END_DATE_BEFORE_START
from apps.events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "start_date_time",
            "end_date_time",
            "image",
            "member_only",
            "lead",
            "description",
            "location",
            "organizer",
            "price",
        ]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("name"),
            FloatingField("start_date_time"),
            FloatingField("end_date_time"),
            FloatingField("location"),
            FloatingField("price"),
            Field("image"),
            FloatingField("organizer"),
            Field("member_only"),
            Field("lead"),
            Field("description"),
        )

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if (
            "start_date_time" in cleaned_data
            and "end_date_time" in cleaned_data
            and cleaned_data["start_date_time"] > cleaned_data["end_date_time"]
        ):
            raise ValidationError("Start time must be after end time", END_DATE_BEFORE_START)
        return cleaned_data
