from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

from apps.core.models.internal import InternalDocument


class InternalDocumentForm(forms.ModelForm):
    class Meta:
        model = InternalDocument
        fields = ["name", "file"]

    def __init__(self, *args, **kwargs):
        super(InternalDocumentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            FloatingField("name"),
            Field("file"),
        )
