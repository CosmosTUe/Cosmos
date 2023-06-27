from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.forms.models import inlineformset_factory

from apps.core.models.gmm import GMM, FileObject


class FileObjectForm(forms.ModelForm):
    class Meta:
        model = FileObject
        fields = ["name", "file"]


GMMFormSet = inlineformset_factory(
    GMM, FileObject, form=FileObjectForm, fields=["name", "file"], extra=1, can_delete=True
)


class GMMFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.form_tag = False
        self.layout = Layout(
            Div(Field("name"), css_class="col col-4"),
            Field("file", wrapper_class="col col-6"),
            Div("DELETE", css_class="col col-2"),
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
            FloatingField("name"),
            FloatingField("date"),
        )
