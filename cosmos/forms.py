from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.forms.models import inlineformset_factory

from cosmos.models import GMM, FileObject, PhotoAlbum


class FileObjectForm(forms.ModelForm):
    class Meta:
        model = FileObject
        exclude = ()


GMMFormSet = inlineformset_factory(
    GMM, FileObject, form=FileObjectForm, fields=["name", "file"], extra=1, can_delete=True
)


class GMMFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.form_tag = False
        self.layout = Layout(
            Field("name", wrapper_class="col-4"),
            Field("file", wrapper_class="col-6"),
            Div("DELETE", css_class="col-2"),
            # Field("DELETE", wrapper_class="col-2"),
        )
        self.render_required_fields = True


class GMMForm(forms.ModelForm):
    class Meta:
        model = GMM
        fields = ["name", "date"]

    def __init__(self, *args, **kwargs):
        super(GMMForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("name"),
            FieldWithButtons(
                "date",
                StrictButton(
                    """<i class="bi bi-calendar-date"></i>""",
                    css_class="btn-outline-secondary",
                    id="id_calendar_button",
                ),
            ),
        )


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
                    css_class="btn-outline-secondary",
                    id="id_calendar_button",
                ),
            ),
            Field("album_cover"),
            Field("photos"),
        )
