from django.contrib.auth.models import Group
from django.db import models


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
    period_from = models.DateField()
    period_to = models.DateField()
    pretix_organizer = models.CharField(max_length=20)
