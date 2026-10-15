from django.db import migrations


def init_newsletter_site(apps, schema_editor):
    newsletter = apps.get_model("newsletter", "Newsletter")
    site = apps.get_model("sites", "Site")
    news = newsletter.objects.get(slug__exact="cosmos-news")
    gmm = newsletter.objects.get(slug__exact="gmm")

    # bit of a hack to make sure that site object exists
    try:
        site.objects.get(id=1)
    except Exception:
        site(pk=1, domain="example.com", name="example.com").save()

    news.site.add(site.objects.get(id=1))
    gmm.site.add(site.objects.get(id=1))


def delete_newsletter_site(apps, schema_editor):
    newsletter = apps.get_model("newsletter", "Newsletter")
    site = apps.get_model("sites", "Site")
    news = newsletter.objects.get(slug__exact="cosmos-news")
    gmm = newsletter.objects.get(slug__exact="gmm")

    news.site.remove(site.objects.get(id=1))
    gmm.site.remove(site.objects.get(id=1))


class Migration(migrations.Migration):
    dependencies = [("cosmos", "0008_default_newsletters"), ("sites", "0002_alter_domain_unique")]

    operations = [migrations.RunPython(init_newsletter_site, delete_newsletter_site)]
