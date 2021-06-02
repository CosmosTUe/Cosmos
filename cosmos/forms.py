from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Field, Layout, Submit
from crispy_forms.bootstrap import StrictButton, FieldWithButtons
from django import forms
from django.forms.models import inlineformset_factory

from cosmos.models import GMM, FileObject


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
            "name",
            "file",
            "DELETE",
            #Button("test", "Add another file", css_class="btn-primary")
        )
        #self.add_input(Button("test", "Add another file", css_class="btn-primary"))
        #self.add_input(Submit("submit", "Create", css_class="btn-primary"))
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
        #self.helper.add_input(Submit("submit", "Create", css_class="btn-primary"))

# class GMMCreateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Field("name"),
#             FieldWithButtons(
#                 "date",
#                 StrictButton(
#                     """<i class="bi bi-calendar-date"></i>""",
#                     css_class="btn-outline-secondary",
#                     id="id_calendar_button",
#                 ),
#             ),
#             Field("slides"),
#             Field("minutes"),
#             Field("files"),
#             HTML("""<a class="btn btn-primary" href="/">Add file</a>"""),
#             FormActions(Submit("submit", "Update", css_class="btn-primary")),
#         )

#     class Meta:
#         model = GMM
#         fields = ["name", "date", "slides", "minutes", "files"]


# class GMMUpdateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Field("name"),
#             FieldWithButtons(
#                 "date",
#                 StrictButton(
#                     """<i class="bi bi-calendar-date"></i>""",
#                     css_class="btn-outline-secondary",
#                     id="id_calendar_button",
#                 ),
#             ),
#             Field("slides"),
#             Field("minutes"),
#             Field("files"),
#             FormActions(Submit("submit", "Update", css_class="btn-primary")),
#         )

#     class Meta:
#         model = GMM
#         fields = ["name", "date", "slides", "minutes", "files"]


# class GMMDeleteForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.add_input(Submit("submit", "Delete", css_class="btn-primary"))

#     class Meta:
#         model = GMM
#         fields = []
