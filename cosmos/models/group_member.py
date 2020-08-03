from django.contrib.auth.models import Group, User
from django.db import models

ROLES = [
    "General Member",
    "Chairperson",
    "Secretary",
    "Treasurer",
    "Internal Affairs",
    "External Affairs",
]


class GroupMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default=ROLES[0], choices=list(enumerate(ROLES)))

    def __str__(self):
        return f"{self.user.first_name}: {self.group.name} - {self.role}"
