from django.contrib.auth.models import User
from django.db import models

from apps.users.models.user.constants import NATIONALITIES


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

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"{self.username}"
