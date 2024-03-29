import datetime

import bs4
from bs4 import BeautifulSoup
from django.contrib.auth.models import Group, Permission, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import make_aware

from apps.events.errors import END_DATE_BEFORE_START, REQUIRED
from apps.events.forms import EventForm
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

    def test_accessible_for_user_with_permission(self):
        user = User.objects.create_user(
            username="user@student.tue.nl", email="user@cosmostue.nl", password="usersecret"
        )
        user.user_permissions.add(
            Permission.objects.get(codename="add_event"),
        )
        self.client.login(username="user@student.tue.nl", password="usersecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

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
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=16, minute=36)),
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
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=16, minute=36)),
            member_only=True,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.member.save()

    def tearDown(self) -> None:
        Event.objects.all().delete()
        Group.objects.all().delete()

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

    def test_user_with_permission_view(self):
        user = User.objects.create_user(
            username="user@student.tue.nl", email="user@cosmostue.nl", password="usersecret"
        )
        user.user_permissions.add(
            Permission.objects.get(codename="view_event"),
        )
        self.client.login(username="user@student.tue.nl", password="usersecret")

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
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=16, minute=36)),
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
            start_date_time=make_aware(datetime.datetime(2201, 1, 1, hour=1, minute=20)),
            end_date_time=make_aware(datetime.datetime(2201, 1, 1, hour=16, minute=36)),
            member_only=True,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.member.save()

    def tearDown(self) -> None:
        Event.objects.all().delete()
        Group.objects.all().delete()

    def assert_event_card_visible(
        self,
        event_object: bs4.Tag,
        name: str,
        start_date_time: str,
        end_date_time: str,
        can_change=False,
        can_delete=False,
    ):
        self.assertEqual(name, event_object.find("h5", {"class": "card-title"}).contents[0])

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
        grid = html_parser.find("div", id="EventGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(1, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", "2200-01-01 16:36", False, False)

    def test_member_view(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="EventGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(2, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", False, False)
        self.assert_event_card_visible(events[1], "Member Event", "2201-01-01 01:20", False, False)

    def test_user_with_permission_view(self):
        user = User.objects.create_user(
            username="user@student.tue.nl", email="user@cosmostue.nl", password="usersecret"
        )
        user.user_permissions.add(
            Permission.objects.get(codename="add_event"),
            Permission.objects.get(codename="change_event"),
            Permission.objects.get(codename="delete_event"),
            Permission.objects.get(codename="view_event"),
        )
        self.client.login(username="user@student.tue.nl", password="usersecret")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="EventGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(2, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", True, True)
        self.assert_event_card_visible(events[1], "Member Event", "2201-01-01 01:20", True, True)

    def test_admin_view(self):
        User.objects.create_superuser(
            username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood"
        )
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="EventGrid")
        events = grid.find_all("div", {"class": "col"})

        self.assertEqual(2, len(events))
        self.assert_event_card_visible(events[0], "Public Event", "2200-01-01 01:20", True, True)
        self.assert_event_card_visible(events[1], "Member Event", "2201-01-01 01:20", True, True)


class EventsUpdateViewTest(TestCase):
    url = "/events/1/update/"

    def setUp(self) -> None:
        self.organizer = Group(name="organizer")
        self.organizer.save()
        self.public = Event(
            pk=1,
            name="Public Event",
            image=get_image_file(),
            description="Public Event description",
            lead="Public Event Lead",
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=30)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=16, minute=36)),
            member_only=False,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.public.save()

    def tearDown(self) -> None:
        Event.objects.all().delete()
        Group.objects.all().delete()

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_user_with_permission_view(self):
        user = User.objects.create_user(
            username="user@student.tue.nl", email="user@cosmostue.nl", password="usersecret"
        )
        user.user_permissions.add(
            Permission.objects.get(codename="change_event"),
        )
        self.client.login(username="user@student.tue.nl", password="usersecret")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(200, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(200, response.status_code)


class EventsDeleteViewTest(TestCase):
    url = "/events/1/delete/"

    def setUp(self) -> None:
        self.organizer = Group(name="organizer")
        self.organizer.save()
        self.public = Event(
            pk=1,
            name="Public Event",
            image=get_image_file(),
            description="Public Event description",
            lead="Public Event Lead",
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=30)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, hour=16, minute=36)),
            member_only=False,
            location="Common Room",
            organizer=self.organizer,
            price=69.69,
        )
        self.public.save()

    def tearDown(self) -> None:
        Event.objects.all().delete()
        Group.objects.all().delete()

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(403, response.status_code)

    def test_user_with_permission_view(self):
        user = User.objects.create_user(
            username="user@student.tue.nl", email="user@cosmostue.nl", password="usersecret"
        )
        user.user_permissions.add(
            Permission.objects.get(codename="delete_event"),
        )
        self.client.login(username="user@student.tue.nl", password="usersecret")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(200, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url, follow=True)

        self.assertEqual(200, response.status_code)


class EventFormTest(TestCase):
    @staticmethod
    def generate_form(
        name="Name",
        start_date_time=None,
        end_date_time=None,
        image=None,
        member_only=False,
        lead="Lead",
        description="Description",
        location="Location",
        organizer=None,
        price=20.0,
    ) -> EventForm:
        if start_date_time is None:
            start_date_time = make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20))
        if end_date_time is None:
            end_date_time = make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20))

        if organizer is None:
            organizer = Group(name="organizer-group").save()
        files = {}
        if image is None:
            upload_image = get_image_file()
            files["image"] = SimpleUploadedFile(upload_image.name, upload_image.read())

        return EventForm(
            data={
                "name": name,
                "start_date_time": start_date_time,
                "end_date_time": end_date_time,
                "member_only": member_only,
                "lead": lead,
                "description": description,
                "location": location,
                "organizer": organizer,
                "price": price,
            },
            files=files,
        )

    @staticmethod
    def generate_missing_fields_form(*fields):
        data = {
            "name": "Name",
            "start_date_time": make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20)),
            "end_date_time": make_aware(datetime.datetime(2200, 1, 1, hour=1, minute=20)),
            "member_only": True,
            "lead": "Lead",
            "description": "Description",
            "location": "Location",
            "organizer": Group(name="organizer-group").save(),
            "price": 42.0,
        }
        upload_image = get_image_file()
        files = {"image": SimpleUploadedFile(upload_image.name, upload_image.read())}

        for field in fields:
            if field in data:
                del data[field]
            if field in files:
                del files[field]
        return EventForm(data=data, files=files)

    def tearDown(self) -> None:
        Group.objects.all().delete()

    def test_success(self):
        form_start_end = self.generate_form()

        # image: required
        # organizer: select from available choices
        self.assertTrue(form_start_end.is_valid())

    def test_empty_start_time(self):
        form = self.generate_missing_fields_form("start_date_time")

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("start_date_time", REQUIRED))

    def test_empty_end_time(self):
        form = self.generate_missing_fields_form("end_date_time")

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("end_date_time", REQUIRED))

    def test_empty_description(self):
        form = self.generate_missing_fields_form("description")

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error("description", REQUIRED))

    def test_start_before_end(self):
        form_end_start = self.generate_form(start_date_time="2200-01-03 01:20", end_date_time="2200-01-01 01:20")

        # image: required
        # [ValidationError(['Start time must be after end time'])]
        self.assertFalse(form_end_start.is_valid())
        self.assertTrue(form_end_start.has_error("__all__", END_DATE_BEFORE_START))
