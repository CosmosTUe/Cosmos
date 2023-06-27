from django.db import models
from django.urls import reverse


class PhotoAlbum(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    album_cover = models.ImageField(upload_to="photos")

    def __str__(self):
        return "PhotoAlbum: {" + self.title + "}"

    def get_absolute_url(self):
        return reverse("cosmos_core:photo_album-list")


class PhotoObject(models.Model):
    photo = models.ImageField(upload_to="photos")
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name="has_photos")

    def __str__(self):
        return "PhotoObject: {" + str(self.photo) + "}"
