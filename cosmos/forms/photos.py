import datetime

from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.exceptions import ValidationError

from cosmos.models import PhotoAlbum, PhotoObject


class PhotoAlbumForm(forms.ModelForm):
    photos = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=False)

    class Meta:
        model = PhotoAlbum
        fields = ["title", "date", "album_cover"]

    def __init__(self, *args, **kwargs):
        super(PhotoAlbumForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("title"),
            FieldWithButtons(
                "date",
                StrictButton(
                    """<i class="bi bi-calendar-date"></i>""",
                    css_class="btn-outline-light",
                    id="id_calendar_button",
                ),
            ),
            Field("album_cover"),
            Field("photos"),
        )

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date > datetime.date.today():
            raise ValidationError(
                "Please set the date of the photo album to a date in the past.", PHOTO_ALBUM_FUTURE_DATE
            )
        return date


class PhotoAlbumUpdateForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ["title", "date", "album_cover"]

    def __init__(self, *args, **kwargs):
        super(PhotoAlbumUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("title"),
            FieldWithButtons(
                "date",
                StrictButton(
                    """<i class="bi bi-calendar-date"></i>""",
                    css_class="btn-outline-light",
                    id="id_calendar_button",
                ),
            ),
            Field("album_cover"),
        )


class PhotoObjectForm(forms.ModelForm):
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}), required=True)

    class Meta:
        model = PhotoObject
        fields = ["photo"]

    def __init__(self, *args, **kwargs):
        super(PhotoObjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Field("photo"))


PHOTO_ALBUM_FUTURE_DATE = "future_photo_album"
