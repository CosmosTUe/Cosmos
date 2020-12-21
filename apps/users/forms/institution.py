from django import forms

from apps.users.models.user.constants import FONTYS_STUDIES, TUE_DEPARTMENTS, TUE_PROGRAMS
from apps.users.models.user.institution import InstitutionFontys, InstitutionTue


class InstitutionTueForm(forms.ModelForm):

    department = forms.ChoiceField(
        choices=list(zip(TUE_DEPARTMENTS, TUE_DEPARTMENTS)), initial="Please select your department"
    )
    program = forms.ChoiceField(choices=list(zip(TUE_PROGRAMS, TUE_PROGRAMS)), initial="Please select your department")

    class Meta:
        model = InstitutionTue
        fields = ["department", "program"]


class InstitutionFontysForm(forms.ModelForm):

    study = forms.ChoiceField(choices=list(zip(FONTYS_STUDIES, FONTYS_STUDIES)), initial="Please select your study")

    class Meta:
        model = InstitutionFontys
        fields = ["study"]
