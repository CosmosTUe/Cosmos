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


class CommitteeSubpageTest(TestCase):
    def setUp(self):
        self.committee = Committee.objects.create(
            group=Group.objects.create(name="Committee - Bar"), slug="bar", display_name="Bar"
        )

    def test_shows_members_and_contact(self):
        self.committee.members = ["Ada Lovelace", "Alan Turing"]
        self.committee.contact_name = "Ada Lovelace"
        self.committee.contact_email = "bar@cosmostue.nl"
        self.committee.save()
        response = self.client.get("/committees/bar/")
        self.assertContains(response, "<li>Ada Lovelace</li>", html=True)
        self.assertContains(response, "<li>Alan Turing</li>", html=True)
        self.assertContains(response, '<a href="mailto:bar@cosmostue.nl">bar@cosmostue.nl</a>', html=True)

    def test_leaves_out_empty_sections(self):
        response = self.client.get("/committees/bar/")
        self.assertNotContains(response, "committee-detail-heading")
