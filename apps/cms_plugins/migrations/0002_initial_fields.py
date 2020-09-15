# Generated by Django 3.0.8 on 2020-09-14 15:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cms_plugins", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="committeesubpagetitlepluginmodel",
            name="committee",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="users.Committee"),
        ),
        migrations.AddField(
            model_name="committeelistpluginmodel",
            name="committees",
            field=models.ManyToManyField(to="users.Committee"),
        ),
        migrations.AddField(
            model_name="boardsubpagetitlepluginmodel",
            name="board",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="users.Board"),
        ),
        migrations.AddField(
            model_name="boardlistpluginmodel",
            name="boards",
            field=models.ManyToManyField(to="users.Board"),
        ),
    ]