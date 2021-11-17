from django.contrib.auth.models import User
from django.test import TestCase

from apps.core.models.photos import PhotoAlbum
from tests.cosmos.helpers import get_image_file


class PhotoAlbumCreateViewTest(TestCase):
    url = "/photos/create/"

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


class PhotoAlbumListViewTest(TestCase):
    url = "/photos/list/"

    def test_success_blank_db(self):
        # setup
        exp_status_code = 200

        # act
        response = self.client.get(self.url)

        # test
        self.assertEqual(exp_status_code, response.status_code)


class PhotoAlbumViewsTest(TestCase):
    # NOTE: Albums cannot have a future date, thus testing visibility for future dates is unnecessary
    url = "/photos/1/"

    def setUp(self) -> None:
        PhotoAlbum(pk=1, title="Borrel", date="2010-10-21", album_cover=get_image_file()).save()

    def test_album_view_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

    def test_album_view_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)

    def test_album_view_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)


class PhotoAlbumAddPhotoViewTest(TestCase):
    url = "/photos/1/add/"

    def setUp(self) -> None:
        PhotoAlbum(pk=1, title="Borrel", date="2010-10-21", album_cover=get_image_file()).save()

    def test_album_view_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_album_view_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_album_view_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)


class PhotoAlbumUpdateViewTest(TestCase):
    url = "/photos/1/update/"

    def setUp(self) -> None:
        PhotoAlbum(pk=1, title="Borrel", date="2010-10-21", album_cover=get_image_file()).save()

    def test_album_view_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_album_view_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_album_view_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)


class PhotoAlbumDeleteViewTest(TestCase):
    url = "/photos/1/delete/"

    def setUp(self) -> None:
        PhotoAlbum(pk=1, title="Borrel", date="2010-10-21", album_cover=get_image_file()).save()

    def test_album_view_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_album_view_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_album_view_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
        album = PhotoAlbum.objects.get(pk=1)
        self.assertIsNotNone(album, "no deletion prior to clicking confirmation button")
