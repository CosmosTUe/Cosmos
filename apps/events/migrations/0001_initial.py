# Generated by Django 3.2.6 on 2021-09-18 21:59

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='events')),
                ('description', ckeditor.fields.RichTextField()),
                ('lead', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('member_only', models.BooleanField()),
                ('location', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('organizer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group')),
            ],
        ),
    ]