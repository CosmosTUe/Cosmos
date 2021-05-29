from django import forms

from cosmos.models import GMM


class GMMCreateForm(forms.ModelForm):
    class Meta:
        model = GMM
        fields = ["name", "date", "slides", "minutes"]
        widgets = {
            "slides": forms.FileInput(),
            "minutes": forms.FileInput(),
        }


class GMMUpdateForm(forms.ModelForm):
    class Meta:
        model = GMM
        fields = ["name", "date", "slides", "minutes"]
        widgets = {
            "slides": forms.FileInput(),
            "minutes": forms.FileInput(),
        }


class GMMDeleteForm(forms.ModelForm):
    class Meta:
        model = GMM
        fields = []
        widgets = {
            "slides": forms.FileInput(),
            "minutes": forms.FileInput(),
        }
