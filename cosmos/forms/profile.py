from cms.utils.compat.forms import UserChangeForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from cosmos.models.user import Profile


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class MemberCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class MemberUpdateForm(UserChangeForm):
    username = forms.EmailField(
        max_length=254, label="TU/e email", help_text="Required. Inform a valid TU/e email address."
    )
    email = forms.EmailField(
        max_length=254, label="Personal email", required=False, help_text="Optional. Inform a valid email address."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["nationality", "department", "program"]

    def save(self, user_ref):
        self.instance.user = user_ref
        return super().save()


class ProfileUpdateForm(ProfileCreateForm):
    class Meta:
        model = Profile
        fields = [
            "nationality",
            "department",
            "program",
            "tue_id",
            "card_number",
            "member_type",
            "key_access",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["member_type"].disabled = True
        self.fields["key_access"].disabled = True
