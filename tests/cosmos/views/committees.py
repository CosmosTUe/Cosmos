from django.contrib.auth.models import Group
from django.test import TestCase

from apps.users.models import Committee


class CommitteeOverviewTest(TestCase):
    def setUp(self):
        Committee.objects.create(
            group=Group.objects.create(name="Committee - Intro"),
            slug="intro",
            display_name="Intro",
            description="Organises the intro week.",
        )
        Committee.objects.create(
            group=Group.objects.create(name="Committee - Goon"), slug="goon", display_name="Goon", hidden=True
        )

    def test_lists_visible_committees(self):
        response = self.client.get("/committees/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/committees/intro/"')
        self.assertContains(response, "Organises the intro week.")
        self.assertNotContains(response, "/committees/goon/")

    def test_committee_without_photo_shows_its_initial(self):
        response = self.client.get("/committees/")
        self.assertContains(response, '<span class="committee-card-initial" aria-hidden="true">I</span>', html=True)
