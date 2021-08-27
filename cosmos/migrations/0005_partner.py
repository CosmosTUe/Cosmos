# Generated by Django 3.2.4 on 2021-08-27 23:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosmos", "0004_testimonial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Partner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField()),
                (
                    "image",
                    models.FileField(
                        upload_to="partners",
                        validators=[django.core.validators.FileExtensionValidator(["svg", "jpg", "png"])],
                    ),
                ),
                ("url", models.URLField(default="#")),
            ],
        ),
    ]
