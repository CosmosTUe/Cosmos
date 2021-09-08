import math

from django.contrib.auth.models import Group
from django.core.validators import FileExtensionValidator, ValidationError
from django.db import models


def validate_aspect_ratio(image):
    ratio = 1 / 1
    if not math.isclose(image.width / image.height, ratio, rel_tol=1e-6):
        raise ValidationError("The aspect ratio is not correct. The aspect ratio should be: " + str(ratio))


class Committee(models.Model):
    """
    Extension of Django Group model to store extra data of committees.

    - `name`, `permissions`: self-explanatory

    To get all groups of a user you can do this:

    - user.groups.all()

    To get all users of a group:

    - group.user_set.all()
    """

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    pretix_team_token = models.CharField(max_length=64, blank=True)
    display_name = models.CharField(max_length=50, blank=False, default="None")
    slug = models.SlugField(blank=False, unique=True, default="None")

    photo = models.FileField(
        upload_to="committees",
        default="committees/default.png",
        validators=[FileExtensionValidator(["svg", "jpg", "jpeg", "png"])],
    )

    @property
    def name(self):
        return self.group.name

    @property
    def permissions(self):
        return self.group.permissions

    def __str__(self):
        return f"{self.name}: {self.description}"
