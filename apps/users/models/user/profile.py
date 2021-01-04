from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models.user.constants import DEPARTMENTS, NATIONALITIES, NEWSLETTER_RECIPIENTS, PROGRAMS

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
    department = models.CharField(max_length=100, blank=False, choices=list(zip(DEPARTMENTS, DEPARTMENTS)))
    program = models.CharField(max_length=100, blank=False, choices=list(zip(PROGRAMS, PROGRAMS)))
    nationality = models.CharField(max_length=100, blank=False, choices=list(zip(NATIONALITIES, NATIONALITIES)))
    tue_id = models.CharField(verbose_name="TU/e Number", blank=True, max_length=25)
    card_number = models.CharField(max_length=25, blank=True)
    key_access = models.BooleanField(max_length=3, default=False)
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

    def __str__(self):
        return f"{self.tue_id}: {self.username}"


@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created, **kwargs):
    """
    Django Signals triggered after User has been saved
    """
    if created:
        # Create a new profile if new instance of User was created
        Profile.objects.create(user=instance)
    # Save user profile
    instance.profile.save()
