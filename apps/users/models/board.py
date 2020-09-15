import math

from django.contrib.auth.models import Group
from django.core.validators import ValidationError
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


def validate_aspect_ratio(image):
    ratio = 1.5
    if not math.isclose(image.width / image.height, ratio, rel_tol=1e-6):
        raise ValidationError("The aspect ratio is not correct. The aspect ratio should be: " + str(ratio))


class Board(models.Model):
    """
    Extension of Django Group modelt to store extra data of the board.

    - `name`, `permissions`: self-explanatory

    To get all groups of a user you can do this:

    - user.groups.all()

    To get all users of a group:

    - group.user_set.all()
    """

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    period_from = models.DateField(blank=False)
    period_to = models.DateField()
    pretix_organizer_token = models.CharField(max_length=20, blank=True)
    members = ArrayField(models.CharField(max_length=100, blank=True), blank=True, default=list)
    display_name = models.CharField(max_length=50, blank=False, default="None")

    photo = models.ImageField(upload_to="boards", default="boards/default.jpg", validators=[validate_aspect_ratio],)

    @property
    def name(self):
        return self.group.name

    @property
    def permissions(self):
        return self.group.permissions

    def __str__(self):
        return f"{self.name}: {self.description}"
