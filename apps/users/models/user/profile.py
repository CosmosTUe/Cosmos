from django.contrib.auth.models import User
from django.db import models

from apps.users.models.user.constants import NATIONALITIES, NEWSLETTER_RECIPIENTS

state_prefix = "old_"


class Profile(models.Model):
    """
    Extension of Django User model to store extra data of users.
    Fields from Django user model are to be interpreted as follows:

    - `username`: TU/e email of the user; ensures uniqueness; mandatory
    - `email`: personal email of the user (Optional)
    - `first_name`, `last_name`, `password`: self-explanatory
    - `group`: committees the user is a part of
    - `is_staff`: user can access admin site (Board and Digital committee)
    - `is_active`: set to False to "delete";

    For more information, please refer to `documentation <https://docs.djangoproject.com/en/3.0/ref/contrib/auth/>`_

    Custom Profile model created to add extra attributes of a user. Default values correspond to values
    for new users.
    """

    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=100, blank=False, choices=list(zip(NATIONALITIES, NATIONALITIES)))
    terms_confirmed = models.BooleanField(default=False)
    subscribed_newsletter = models.BooleanField(default=False)
    newsletter_recipient = models.CharField(
        max_length=3, verbose_name="Newsletter subscription email", default="TUE", choices=NEWSLETTER_RECIPIENTS
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.states = ["subscribed_newsletter", "newsletter_recipient"]
        self.update_states()

    def update_states(self):
        for state in self.states:
            setattr(self, f"{state_prefix}{state}", getattr(self, state))

    def has_changed(self):
        for state in self.states:
            if getattr(self, state) != getattr(self, f"{state_prefix}{state}"):
                return True
        return False

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    @property
    def institution(self):
        from apps.users.models.user.institution import InstitutionFontys, InstitutionTue

        if self.user.username.endswith("tue.nl"):
            return InstitutionTue.objects.get(profile=self)
        elif self.user.username.endswith("fontys.nl"):
            return InstitutionFontys.objects.get(profile=self)
        return None

    @property
    def institution_name(self):
        if self.user.username.endswith("tue.nl"):
            return "tue"
        elif self.user.username.endswith("fontys.nl"):
            return "fontys"
        return None

    def __str__(self):
        return f"{self.username}"
