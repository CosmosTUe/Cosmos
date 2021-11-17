from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms

from apps.core.models.news import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "publish_date", "image", "member_only", "lead", "content"]

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field("title"),
            Field("publish_date"),
            Field("image"),
            Field("member_only"),
            Field("lead"),
            Field("content"),
        )
