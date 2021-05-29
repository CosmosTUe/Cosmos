from django.db import models
from django.urls import reverse


class GMM(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    slides = models.FileField(null=True, blank=True)
    minutes = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name + " - " + str(self.date)

    def get_absolute_url(self):
        return reverse("resources")
