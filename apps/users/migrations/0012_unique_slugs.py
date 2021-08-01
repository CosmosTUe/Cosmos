# Generated by Django 3.2.4 on 2021-07-23 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0011_cleanup_group_models"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board",
            name="slug",
            field=models.SlugField(default="None", unique=True),
        ),
        migrations.AlterField(
            model_name="committee",
            name="slug",
            field=models.SlugField(default="None", unique=True),
        ),
    ]