import datetime

from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.core.exceptions import ValidationError

from apps.core.models.photos import PhotoAlbum, PhotoObject


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PhotoAlbumForm(forms.ModelForm):
    photos = MultipleImageField(widget=MultipleFileInput(), required=False)

    class Meta:
        model = PhotoAlbum
        fields = ["title", "date", "album_cover"]

    def __init__(self, *args, **kwargs):
        super(PhotoAlbumForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("title"),
            FloatingField("date"),
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
            FloatingField("title"),
            FloatingField("date"),
            Field("album_cover"),
        )


class PhotoObjectForm(forms.ModelForm):
    photos = forms.ImageField(widget=MultipleFileInput(), required=True)

    class Meta:
        model = PhotoObject
        fields = ["photos"]

    def __init__(self, *args, **kwargs):
        super(PhotoObjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(Field("photos"))


PHOTO_ALBUM_FUTURE_DATE = "future_photo_album"
