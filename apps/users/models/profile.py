from django.contrib.auth.models import User
from django.db import models

from apps.users.helper_functions import is_fontys_email, is_tue_email
from apps.users.models.constants import NATIONALITIES, NEWSLETTER_RECIPIENTS


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

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    @property
    def institution(self):
        from apps.users.models.institution import InstitutionFontys, InstitutionTue

        if is_tue_email(self.username):
            return InstitutionTue.objects.get(profile=self)
        elif is_fontys_email(self.username):
            return InstitutionFontys.objects.get(profile=self)
        return None

    @property
    def institution_name(self):
        if is_tue_email(self.username):
            return "tue"
        elif is_fontys_email(self.username):
            return "fontys"
        return None

    def __str__(self):
        return f"{self.username}"
