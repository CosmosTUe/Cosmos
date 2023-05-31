from django.contrib.sites.models import Site
from django.db import migrations
from newsletter.models import Newsletter


def init_newsletter_site(apps, schema_editor):
    news = Newsletter.objects.get(slug__exact="cosmos-news")
    gmm = Newsletter.objects.get(slug__exact="gmm")

    # bit of a hack to make sure that site object exists
    try:
        Site.objects.get(id=1)
    except Exception:
        Site(pk=1, domain="example.com", name="example.com").save()

    news.site.add(Site.objects.get(id=1))
    gmm.site.add(Site.objects.get(id=1))


def delete_newsletter_site(apps, schema_editor):
    news = Newsletter.objects.get(slug__exact="cosmos-news")
    gmm = Newsletter.objects.get(slug__exact="gmm")

    news.site.remove(Site.objects.get(id=1))
    gmm.site.remove(Site.objects.get(id=1))


class Migration(migrations.Migration):
    dependencies = [("cosmos", "0008_default_newsletters"), ("sites", "0002_alter_domain_unique")]

    operations = [migrations.RunPython(init_newsletter_site, delete_newsletter_site)]
