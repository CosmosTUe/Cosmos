# Generated by Django 3.2.6 on 2021-09-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosmos", "0005_partner"),
    ]

    operations = [
        migrations.CreateModel(
            name="Token",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("token", models.CharField(max_length=100)),
                ("device", models.CharField(max_length=50)),
            ],
        ),
    ]
