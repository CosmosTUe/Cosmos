import datetime

from django.contrib.auth.models import Group
from django.test import TestCase

from apps.core.models import News
from apps.users.models import Committee


class SitemapTest(TestCase):
    def setUp(self):
        Committee.objects.create(
            group=Group.objects.create(name="Committee - Intro"), slug="intro", display_name="Intro"
        )
        Committee.objects.create(
            group=Group.objects.create(name="Committee - Goon"), slug="goon", display_name="Goon", hidden=True
        )
        today = datetime.date.today()
        for title, member_only, publish_date in (
            ("Public", False, today),
            ("Members", True, today),
            ("Upcoming", False, today + datetime.timedelta(days=7)),
        ):
            News.objects.create(
                title=title, image="news/x.png", content="", publish_date=publish_date, member_only=member_only
            )

    def test_sitemap_lists_public_pages(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/about/")
        self.assertContains(response, "/committees/intro/")
        self.assertContains(response, "/news/%d/" % News.objects.get(title="Public").pk)

    def test_sitemap_leaves_out_hidden_and_non_public_content(self):
        response = self.client.get("/sitemap.xml")
        self.assertNotContains(response, "/committees/goon/")
        self.assertNotContains(response, "/news/%d/" % News.objects.get(title="Members").pk)
        self.assertNotContains(response, "/news/%d/" % News.objects.get(title="Upcoming").pk)
