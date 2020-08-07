from django.contrib.auth.models import Group
from django.db import models

from cosmos.models.board import Board


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
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    pretix_team_token = models.CharField(max_length=64)

    photo = models.ImageField(upload_to="committees", default="boards/default.jpg")

    @property
    def name(self):
        return self.group.name

    @property
    def permissions(self):
        return self.group.permissions

    def __str__(self):
        return f"{self.name}: {self.description}"
