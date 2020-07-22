from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from cosmos.models.user.constants import DEPARTMENTS, NATIONALITIES, PROGRAMS


class Profile(models.Model):
    """
    Extension of Django User model to store extra data of users.
    Fields from Django user model are to be interpretted as follows:

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

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, choices=((name, name) for name in DEPARTMENTS))
    program = models.CharField(max_length=100, choices=((name, name) for name in PROGRAMS))
    nationality = models.CharField(max_length=100, choices=((country, country) for country in NATIONALITIES))
    tue_id = models.CharField(verbose_name="TU/e Number", max_length=25)
    card_number = models.CharField(max_length=25)
    key_access = models.CharField(max_length=3, default="No")
    member_type = models.CharField(
        max_length=50, default="Pending", choices=((status, status) for status in ["Member", "Pending", "Rejected"])
    )

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"{self.tue_id}: {self.username}"


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Django Signals triggered after User has been saved
    """
    if created:
        # Create a new profile if new instance of User was created
        Profile.objects.create(user=instance)
    # Save user profile
    instance.profile.save()
