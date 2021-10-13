import datetime

import bs4
from bs4 import BeautifulSoup
from django.contrib.auth.models import Group, User
from django.test import TestCase

from apps.events.models import Event
from tests.cosmos.helpers import get_image_file


class EventsCreateViewTest(TestCase):
    url = "/events/add/"

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)


class EventsViewTest(TestCase):
    def setUp(self) -> None:
        self.organizer = Group(name="organizer")
        self.organizer.save()
        self.public = Event(
            name="Public Event",
            image=get_image_file(),
            description="Public Event description",
            lead="Public Event Lead",
            start_date_time="2200-01-01 01:20",
            end_date_time="2200-01-01 16:36",
            member_only=False,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.public.save()
        self.member = Event(
            name="Member Event",
            image=get_image_file(),
            description="Member Event description",
            lead="Member Event Lead",
            start_date_time="2200-01-01 01:20",
            end_date_time="2200-01-01 16:36",
            member_only=True,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.member.save()

    def tearDown(self) -> None:
        return Event.objects.all().delete()

    def assert_event_view_visible(self, pk):
        url = f"/events/{pk}/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def assert_event_not_found(self, pk):
        url = f"/events/{pk}/"
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def assert_event_member_only(self, pk):
        url = f"/events/{pk}/"
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)

    def test_public_view(self):
        self.client.logout()

        self.assert_event_view_visible(self.public.pk)
        self.assert_event_member_only(self.member.pk)
        self.assert_event_not_found(500)

    def test_member_view(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        self.assert_event_view_visible(self.public.pk)
        self.assert_event_view_visible(self.member.pk)
        self.assert_event_not_found(500)

    def test_admin_view(self):
        User.objects.create_superuser(
            username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood"
        )
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        self.assert_event_view_visible(self.public.pk)
        self.assert_event_view_visible(self.member.pk)
        self.assert_event_not_found(500)


class EventsListViewTest(TestCase):
    url = "/events/list/"

    def setUp(self) -> None:
        self.organizer = Group(name="organizer")
        self.organizer.save()
        self.public = Event(
            name="Public Event",
            image=get_image_file(),
            description="Public Event description",
            lead="Public Event Lead",
            start_date_time="2200-01-01 01:20",
            end_date_time="2200-01-01 16:36",
            member_only=False,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.public.save()
        self.member = Event(
            name="Member Event",
            image=get_image_file(),
            description="Member Event description",
            lead="Member Event Lead",
            start_date_time="2201-01-01 01:20",
            end_date_time="2201-01-01 16:36",
            member_only=True,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.member.save()

    def tearDown(self) -> None:
        return Event.objects.all().delete()

    def assert_event_card_visible(
        self,
        event_object: bs4.Tag,
        name: str,
        start_date_time: str,
        end_date_time: str,
        can_change=False,
        can_delete=False,
    ):
        self.assertEqual(name, event_object.find("h5", {"class": "card-title"})).contents[0]
        date = datetime.datetime.fromisoformat(start_date_time).strftime("%b. %d, %Y, %-I %p")  # default date format
        self.assertEqual(date, event_object.find("small", {"class": "test-muted"}).contents[0].strip())

        event = Event.objects.get(name=name)

        if can_change:
            self.assertEqual(
                f"/events/{event.pk}/update/",
                event_object.find_all("a", {"class": "btn p-0 btn-over-stretched"})[0].get("href"),
            )
        else:
            self.assertIsNone(event_object.find("a", {"class": "btn p-0", "href": f"/events/{event.pk}/update/"}))

        if can_delete:
            self.assertEqual(
                f"/events/{event.pk}/delete/",
                event_object.find_all("a", {"class": "btn p-0 btn-over-stretched"})[1].get("href"),
            )
        else:
            self.assertIsNone(event_object.find("a", {"class": "btn p-0", "href": f"/events/{event.pk}/delete/"}))

    def test_public_view(self):
        self.client.logout()

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="NewsGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(1, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", False, False)

    def test_member_view(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="NewsGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(1, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", False, False)
        self.assert_event_card_visible(events[1], "Public Event", "2201-01-01 01:20", False, False)

    def test_admin_view(self):
        User.objects.create_superuser(
            username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood"
        )
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="NewsGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(1, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", True, True)
        self.assert_event_card_visible(events[1], "Public Event", "2201-01-01 01:20", True, True)


class EventsUpdateViewTest(TestCase):
    url = "/events/1/update"

    def setUp(self) -> None:
        self.organizer = Group(name="organizer")
        self.organizer.save()
        self.public = Event(
            pk=1,
            name="Public Event",
            image=get_image_file(),
            description="Public Event description",
            lead="Public Event Lead",
            start_date_time="2200-01-01 01:20",
            end_date_time="2200-01-01 16:36",
            member_only=False,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )

    def tearDown(self) -> None:
        return Event.objects.all().delete()

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(200, response.status_code)


class EventsDeleteViewTest(TestCase):
    url = "/events/1/delete"

    def setUp(self) -> None:
        self.organizer = Group(name="organizer")
        self.organizer.save()
        self.public = Event(
            pk=1,
            name="Public Event",
            image=get_image_file(),
            description="Public Event description",
            lead="Public Event Lead",
            start_date_time="2200-01-01 01:20",
            end_date_time="2200-01-01 16:36",
            member_only=False,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )

    def tearDown(self) -> None:
        return Event.objects.all().delete()

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(200, response.status_code)
