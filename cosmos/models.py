from crum import get_current_user
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# class FileContainer(models.Model):
#     class Meta:
#         abstract = True


class GMM(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return "GMM: {" + self.name + ", " + str(self.date) + "}"

    def get_absolute_url(self):
        return reverse("resources")


class FileObject(models.Model):
    name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name="created_by"
    )

    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name="modified_by"
    )

    file = models.FileField(null=False, blank=False)

    container = models.ForeignKey(GMM, on_delete=models.CASCADE, related_name="has_files")

    def save(self, *args, **kwargs):
        print("Save called on file object")
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(FileObject, self).save(*args, **kwargs)

    def __str__(self):
        return "FileObject: {" + self.name + ", " + str(self.date) + "}"



