from crum import get_current_user
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class GMM(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    class Meta:
        verbose_name = "GMM"
        verbose_name_plural = "GMMs"

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

    file = models.FileField(null=False, blank=False, upload_to="gmm/")

    container = models.ForeignKey(GMM, on_delete=models.CASCADE, related_name="has_files")

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(FileObject, self).save(*args, **kwargs)

    def __str__(self):
        return "FileObject: {" + self.name + ", " + str(self.date) + "}"


class PhotoAlbum(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    album_cover = models.ImageField(upload_to="photos")

    def get_absolute_url(self):
        return reverse("photo_album-list")

    def __str__(self):
        return "PhotoAlbum: {" + self.title + "}"


class PhotoObject(models.Model):
    photo = models.ImageField(upload_to="photos")
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name="has_photos")

    def __str__(self):
        return "PhotoObject: {" + str(self.photo) + "}"
