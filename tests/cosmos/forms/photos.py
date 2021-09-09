import datetime

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from cosmos.forms import PhotoAlbumForm, PhotoAlbumUpdateForm, PhotoObjectForm
from cosmos.forms.photos import PHOTO_ALBUM_FUTURE_DATE
from cosmos.models import News, PhotoAlbum
from tests.cosmos.helpers import get_image_file


class PhotoAlbumFormTest(TestCase):
    def tearDown(self) -> None:
        News.objects.all().delete()

    @staticmethod
    def generate_form(title="", date="", album_cover: File = None):
        files = {}
        if album_cover is not None:
            files["album_cover"] = SimpleUploadedFile(album_cover.name, album_cover.read())
        return PhotoAlbumForm(
            data={
                "title": title,
                "date": date,
            },
            files=files,
        )

    def test_empty_form(self):
        form = self.generate_form()

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("title", "required"))
        self.assertTrue(form.has_error("date", "required"))
        self.assertTrue(form.has_error("album_cover", "required"))
        self.assertFalse(form.has_error("photos"))

    def test_past_album_is_valid(self):
        form = self.generate_form("Borrel", "2010-10-12", get_image_file())

        self.assertTrue(form.is_valid())
        form.save()

        album = PhotoAlbum.objects.get(title="Borrel")
        self.assertIsNotNone(album)
        self.assertEqual(datetime.date(2010, 10, 12), album.date)

    def test_future_album_is_not_valid(self):
        form = self.generate_form("Borrel", "2100-10-12", get_image_file())

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("date", PHOTO_ALBUM_FUTURE_DATE))


class PhotoAlbumUpdateFormTest(TestCase):
    def test_prefill_data_from_db(self):
        album = PhotoAlbum(title="Borrel", date="2010-10-21", album_cover=get_image_file())

        form = PhotoAlbumUpdateForm(instance=album)

        self.assertEqual("Borrel", form["title"].initial)
        self.assertEqual("2010-10-21", form["date"].initial)


class PhotoObjectFormTest(TestCase):
    def test_empty_form_fails(self):
        form = PhotoObjectForm(data={}, files={})

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("photo", "required"))
        self.assertFalse(form.has_error("album"))  # album is not part of the form, rather part of the model

    def test_success_submission(self):
        img = get_image_file()
        form = PhotoObjectForm(files={"photo": SimpleUploadedFile(img.name, img.read())})

        self.assertTrue(form.is_valid())
