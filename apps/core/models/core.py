from django.db import models


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
