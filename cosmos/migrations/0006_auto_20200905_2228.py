# Generated by Django 3.0.8 on 2020-09-05 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosmos", "0005_committee_board_display_names"),
    ]

    operations = [
        migrations.AlterField(
            model_name="board", name="display_name", field=models.CharField(default="None", max_length=50),
        ),
        migrations.AlterField(
            model_name="committee", name="display_name", field=models.CharField(default="None", max_length=50),
        ),
    ]
