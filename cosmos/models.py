from django.db import models
from filer.fields.file import FilerFileField


class GMM(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    slides = FilerFileField(null=True, blank=True, on_delete=models.CASCADE, related_name="GMM_slides")
    minutes = FilerFileField(null=True, blank=True, on_delete=models.CASCADE, related_name="GMM_minutes")

    def __str__(self):
        return self.name + " - " + str(self.date)
