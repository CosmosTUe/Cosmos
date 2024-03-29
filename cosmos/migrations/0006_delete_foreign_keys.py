# Generated by Django 3.2.7 on 2021-10-13 17:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("cosmos", "0005_partner"), ("core", "0001_initial")]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="fileobject",
                    name="container",
                ),
                migrations.RemoveField(
                    model_name="fileobject",
                    name="created_by",
                ),
                migrations.RemoveField(
                    model_name="fileobject",
                    name="modified_by",
                ),
                migrations.RemoveField(
                    model_name="news",
                    name="author",
                ),
                migrations.RemoveField(
                    model_name="photoobject",
                    name="album",
                ),
            ],
            database_operations=[],
        ),
    ]
