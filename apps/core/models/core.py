from django.db import models

from apps.utils import AspectRatioValidator


class Testimonial(models.Model):
    image = models.ImageField(upload_to="testimonials", blank=True, validators=[AspectRatioValidator(1.0)])
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
