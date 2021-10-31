from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse


class Event(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events")
    description = RichTextField()
    lead = models.TextField()
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    member_only = models.BooleanField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(Group, blank=True, null=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Event: {" + self.name + "}"

    def get_absolute_url(self):
        return "https://cosmostue.nl" + reverse("cosmos_events:events-view", kwargs={"pk": self.pk})
