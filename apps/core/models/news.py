import datetime

from ckeditor.fields import RichTextField
from crum import get_current_user
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


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
