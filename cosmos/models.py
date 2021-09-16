import datetime

from ckeditor.fields import RichTextField
from crum import get_current_user
from django.contrib.auth.models import Group, User
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
        return reverse("gmm-list")


class FileObject(models.Model):
    name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name="gmm_created_by"
    )

    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name="gmm_modified_by"
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
        return "FileObjectGMM: {" + self.name + ", " + str(self.date) + "}"


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


class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="news")
    content = RichTextField()
    lead = models.TextField(blank=True)
    publish_date = models.DateField()
    member_only = models.BooleanField()
    author = models.ForeignKey(
        User, blank=True, null=True, default=None, on_delete=models.SET_NULL, related_name="author"
    )

    def published(self):
        if self.publish_date > datetime.date.today():
            return False
        else:
            return True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk:
            self.author = user
        super(News, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news-list")

    def __str__(self):
        return "News: {" + self.title + ", " + str(self.publish_date) + "}"


class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events")
    description = RichTextField()
    lead = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    member_only = models.BooleanField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "Event: {" + self.name + "}"

    # def get_date(self):
    #     if self.start_time.date() == self.end_time.date()
    #     return


class Testimonial(models.Model):
    text = models.TextField(blank=False)
    author = models.CharField(blank=False, max_length=100)

    def __str__(self):
        return "Testimonial: {" + self.author + "}"


class Partner(models.Model):
    name = models.TextField(blank=False)
    image = models.ImageField(upload_to="partners")
    url = models.URLField(blank=True)

    def __str__(self):
        return "Partner: {" + self.name + "}"
