from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.exceptions import ValidationError

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
            Field("name"),
            FieldWithButtons(
                "start_date_time",
                StrictButton(
                    """<i class="bi bi-calendar-date"></i>""",
                    css_class="btn-outline-light",
                    id="id_calendar_button",
                ),
            ),
            FieldWithButtons(
                "end_date_time",
                StrictButton(
                    """<i class="bi bi-calendar-date"></i>""",
                    css_class="btn-outline-light",
                    id="id_calendar_button",
                ),
            ),
            Field("location"),
            Field("price"),
            Field("image"),
            Field("organizer"),
            Field("member_only"),
            Field("lead"),
            Field("description"),
        )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["start_date_time"] > cleaned_data["end_date_time"]:
            raise ValidationError("Start time must be after end time")