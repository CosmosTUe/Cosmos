# Generated by Django 4.0.8 on 2022-12-19 21:57

from django.db import migrations
from newsletter.models import Newsletter


def init_default_newsletters(apps, schema_editor):
    email = "noreply@cosmostue.nl"
    Newsletter(title="Cosmos News", slug="cosmos-news", email=email, sender="Cosmos").save()
    Newsletter(title="GMM", slug="gmm", email=email, sender="Cosmos Board").save()


def delete_default_newsletters(apps, schema_editor):
    Newsletter.objects.get(slug__exact="cosmos-news").delete()
    Newsletter.objects.get(slug__exact="gmm").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("cosmos", "0007_delete_models"),
        ("newsletter", "0009_auto_20220927_1220"),
    ]

    operations = [migrations.RunPython(init_default_newsletters, delete_default_newsletters)]
