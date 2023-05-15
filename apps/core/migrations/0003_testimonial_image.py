# Generated by Django 4.2 on 2023-05-15 15:32

from django.db import migrations, models

import apps.core.models.core


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_internaldocument"),
        ("cosmos", "0007_delete_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="testimonial",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="testimonials", validators=[apps.core.models.core.validate_aspect_ratio]
            ),
        ),
    ]