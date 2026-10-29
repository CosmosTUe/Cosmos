import datetime
import importlib

from django.apps import apps
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils.timezone import make_aware

from apps.events.models import Event
from tests.cosmos.helpers import get_image_file

copy_permissions = importlib.import_module("apps.core.migrations.0006_copy_old_cosmos_permissions")
remove_stale = importlib.import_module("apps.core.migrations.0007_remove_stale_content_types")


def committee_member(*perms):
    """Logged-in style user (not a superuser) whose group holds exactly these permissions."""
    group = Group.objects.create(name="Committee - Test")
    for perm in perms:
        app_label, codename = perm.split(".")
        group.permissions.add(Permission.objects.get(content_type__app_label=app_label, codename=codename))
    user = User.objects.create_user(username="member@student.tue.nl", password="committeesecret")
    user.groups.add(group)
    return user


class CurrentPermissionNamesTest(TestCase):
    def test_add_pages_open_with_current_permissions(self):
        pages = {
            "/news/add/": "core.add_news",
            "/gmm/add/": "core.add_gmm",
            "/internal/add/": "core.add_internaldocument",
            "/photos/create/": "core.add_photoalbum",
        }
        self.client.force_login(committee_member(*pages.values()))
        for url in pages:
            self.assertEqual(200, self.client.get(url).status_code, url)

    def test_add_pages_closed_without_permissions(self):
        self.client.force_login(committee_member())
        for url in ["/news/add/", "/gmm/add/", "/internal/add/", "/photos/create/"]:
            self.assertEqual(403, self.client.get(url).status_code, url)

    def test_event_page_shows_edit_buttons(self):
        event = Event.objects.create(
            name="Event",
            image=get_image_file(),
            description="<p>Description</p>",
            lead="Lead",
            start_date_time=make_aware(datetime.datetime(2200, 1, 1, 18)),
            end_date_time=make_aware(datetime.datetime(2200, 1, 1, 21)),
            member_only=False,
            location="Common Room",
            price=0,
        )
        self.client.force_login(committee_member("events.change_event", "events.delete_event"))
        response = self.client.get(f"/events/{event.pk}/")
        self.assertContains(response, f"/events/{event.pk}/update/")
        self.assertContains(response, f"/events/{event.pk}/delete/")


class CopyOldPermissionsMigrationTest(TestCase):
    def test_holders_of_old_permissions_get_the_current_ones(self):
        old_type = ContentType.objects.create(app_label="cosmos", model="news")
        old = Permission.objects.create(content_type=old_type, codename="add_news", name="Can add news")
        old_board = Permission.objects.create(
            content_type=ContentType.objects.create(app_label="cosmos", model="board"),
            codename="view_board",
            name="Can view board",
        )
        group = Group.objects.create(name="Board")
        group.permissions.add(old, old_board)
        user = User.objects.create_user(username="old@student.tue.nl")
        user.user_permissions.add(old)

        copy_permissions.copy_old_permissions(apps, None)

        self.assertTrue(group.permissions.filter(content_type__app_label="core", codename="add_news").exists())
        self.assertTrue(group.permissions.filter(content_type__app_label="users", codename="view_board").exists())
        self.assertTrue(User.objects.get(pk=user.pk).has_perm("core.add_news"))


class RemoveStaleContentTypesMigrationTest(TestCase):
    def test_stale_types_go_and_current_ones_stay(self):
        old_news = ContentType.objects.create(app_label="cosmos", model="news")
        old_perm = Permission.objects.create(content_type=old_news, codename="add_news", name="Can add news")
        ContentType.objects.create(app_label="legacy", model="mysitedoor")
        ContentType.objects.create(app_label="users", model="groupmember")
        group = Group.objects.create(name="Board")
        group.permissions.add(old_perm, Permission.objects.get(content_type__app_label="core", codename="add_news"))
        admin = User.objects.create_superuser(username="admin@student.tue.nl")
        entry = LogEntry.objects.create(
            user=admin, content_type=old_news, object_id="1", object_repr="Old news", action_flag=CHANGE
        )

        remove_stale.remove_stale_content_types(apps, None)

        for app_label, model in [("cosmos", "news"), ("legacy", "mysitedoor"), ("users", "groupmember")]:
            self.assertFalse(ContentType.objects.filter(app_label=app_label, model=model).exists())
        self.assertFalse(Permission.objects.filter(pk=old_perm.pk).exists())
        # current types, and the permission the group holds through them, are untouched
        self.assertTrue(ContentType.objects.filter(app_label="users", model="committee").exists())
        self.assertEqual(["add_news"], list(group.permissions.values_list("codename", flat=True)))
        # admin history is kept, without the link to the removed type
        entry.refresh_from_db()
        self.assertIsNone(entry.content_type)
        self.assertEqual("Old news", entry.object_repr)
