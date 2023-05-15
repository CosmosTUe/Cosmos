import math

from django.core.validators import ValidationError
from django.db import models


def validate_aspect_ratio(image):
    ratio = 1
    if not math.isclose(image.width / image.height, ratio, rel_tol=1e-6):
        raise ValidationError("The aspect ratio is not correct. The aspect ratio should be: " + str(ratio))


class Testimonial(models.Model):
    image = models.ImageField(upload_to="testimonials", blank=True, validators=[validate_aspect_ratio])
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
