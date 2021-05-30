from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from cosmos.models import GMM


class GMMCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Create", css_class="btn-primary"))
        # TODO: permissions, datepicker

    class Meta:
        model = GMM
        fields = ["name", "date", "slides", "minutes"]


class GMMUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Update", css_class="btn-primary"))

    class Meta:
        model = GMM
        fields = ["name", "date", "slides", "minutes"]


class GMMDeleteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Delete", css_class="btn-primary"))

    class Meta:
        model = GMM
        fields = []
