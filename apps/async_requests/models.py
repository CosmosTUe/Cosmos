from django.db import models


class CommandModel(models.Model):
    data = models.JSONField(blank=False)

    def __str__(self):
        return str(self.data)
