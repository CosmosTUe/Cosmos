from cms.utils.compat.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm

from cosmos.models.user import Profile


class CosmosMemberChange(UserChangeForm):
    # TODO consider overriding
    pass


class CosmosMemberCreation(UserCreationForm):
    # TODO consider overriding
    pass


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["gender", "nationality", "department", "program", "tue_id", "card_number"]

    def save(self, user_ref):
        self.instance.user = user_ref
        return super().save()


class ProfileChangeForm(ProfileCreationForm):
    class Meta:
        model = Profile
        fields = [
            "gender",
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
