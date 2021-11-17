import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase, TransactionTestCase

from apps.core.models.gmm import GMM, FileObject
from apps.users.forms import error_codes
from apps.users.models import Profile
from cosmos import settings
from tests.cosmos.helpers import clear_temp_files, get_new_file, get_new_gmm


def assert_file_exists(test: TestCase, file_name: str):
    url = f"/media/gmm/{file_name}"
    file_path = f"{settings.MEDIA_ROOT}/gmm/{file_name}"

    response = test.client.get(url)
    test.assertEqual(200, response.status_code, "endpoint shall work")
    test.assertTrue(FileObject.objects.filter(name=file_name).exists(), "file shall be in DB")
    test.assertTrue(os.path.exists(file_path), "file in filesystem")


def assert_file_not_exist(test: TestCase, file_name: str):
    url = f"/media/gmm/{file_name}"
    file_path = f"{settings.MEDIA_ROOT}/gmm/{file_name}"

    response = test.client.get(url)
    test.assertEqual(404, response.status_code, "endpoint shall fail")
    test.assertFalse(FileObject.objects.filter(name=file_name).exists(), "file shall not be in DB")
    test.assertFalse(os.path.exists(file_path), "file is not in filesystem")


def get_test_gmm(name="TestGMM", date="2010-10-21", files=None):
    """
    Shortcut to create test GMM object

    :param name:
    :param date:
    :param files: list of file names
    :return: Tuple of GMM object and list of FileObject's
    """
    if files is None:
        files = ["test.md"]

    gmm = get_new_gmm(name, date)
    output = []
    for name in files:
        obj = get_new_file_object(name, File(get_new_file(name)), gmm)
        output.append(obj)
    return gmm, output


def get_new_file_object(name="test file", file=None, gmm=None):
    """
    Shortcut to create new default FileObject object

    :param name: Label for file object
    :param file: File stream (IO object)
    :param gmm: GMM object. See `get_new_gmm()` for default
    :return: FileObject object
    """
    if file is None:
        file = get_new_file("test.md")
    if gmm is None:
        gmm = get_new_gmm()
    return FileObject.objects.create(name=name, file=File(file), container=gmm)


class GMMViewsTestAdminLoggedIn(TransactionTestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

    def tearDown(self) -> None:
        GMM.objects.all().delete()
        FileObject.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        clear_temp_files()
        super().tearDownClass()

    def test_success_list_empty(self):
        # setup
        url = "/gmm/list/"

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Switch view")
        self.assertContains(response, "Add new GMM")

    def test_success_show_add_view(self):
        # setup
        url = "/gmm/add/"

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(200, response.status_code)

    def test_fail_submit_empty_add_view(self):
        # setup
        url = "/gmm/add/"

        # act
        response = self.client.post(url, {"name": "", "date": ""})

        # test
        self.assertEqual(200, response.status_code)
        form = response.context_data["form"]
        self.assertTrue(form.has_error("name", error_codes.REQUIRED))
        self.assertTrue(form.has_error("date", error_codes.REQUIRED))

    def test_success_submit_no_files_add_view(self):
        # setup
        url = "/gmm/add/"

        # act
        response = self.client.post(
            url,
            {
                "name": "A",
                "date": "2021-07-28",
                "has_files-TOTAL_FORMS": 1,
                "has_files-INITIAL_FORMS": 0,
                "submit": "Create",
            },
        )

        # test
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, "/gmm/list/")

    def test_success_submit_one_file_add_view(self):
        # setup
        url = "/gmm/add/"

        # act
        with get_new_file("test.md") as test_file:
            response = self.client.post(
                url,
                {
                    "name": "A",
                    "date": "2021-07-28",
                    "has_files-TOTAL_FORMS": 1,
                    "has_files-INITIAL_FORMS": 0,
                    "has_files-MIN_NUM_FORMS": 0,
                    "has_files-MAX_NUM_FORMS": 1000,
                    "has_files-0-id": "",
                    "has_files-0-name": "test.md",
                    "has_files-0-file": test_file,
                    "submit": "Create",
                },
            )

        # test
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, "/gmm/list/")
        assert_file_exists(self, "test.md")

    def test_success_submit_two_files_add_view(self):
        # setup
        url = "/gmm/add/"

        # act
        with get_new_file("test.md") as md, get_new_file("img.png") as img:
            response = self.client.post(
                url,
                {
                    "name": "A",
                    "date": "2021-07-28",
                    "has_files-TOTAL_FORMS": 2,
                    "has_files-INITIAL_FORMS": 0,
                    "has_files-MIN_NUM_FORMS": 0,
                    "has_files-MAX_NUM_FORMS": 1000,
                    "has_files-0-id": "",
                    "has_files-0-name": "test.md",
                    "has_files-0-file": md,
                    "has_files-1-id": "",
                    "has_files-1-name": "img.png",
                    "has_files-1-file": img,
                    "submit": "Create",
                },
            )

        # test
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, "/gmm/list/")
        assert_file_exists(self, "test.md")
        assert_file_exists(self, "img.png")

    def test_success_update_gmm_delete_file(self):
        # setup
        gmm, files = get_test_gmm("GMM Update", "2010-12-31", ["test.md", "test_image.png"])
        url = f"/gmm/{gmm.pk}/update"

        # act
        response = self.client.post(
            url,
            {
                "name": "GMM Update",
                "date": "2010-12-31",
                "has_files-TOTAL_FORMS": 3,
                "has_files-INITIAL_FORMS": 2,
                "has_files-MIN_NUM_FORMS": 0,
                "has_files-MAX_NUM_FORMS": 1000,
                "has_files-0-id": files[0].pk,
                "has_files-0-name": files[0].name,
                "has_files-0-file": files[0].file,
                "has_files-1-id": files[1].pk,
                "has_files-1-name": files[1].name,
                "has_files-1-file": files[1].file,
                "has_files-1-DELETE": "on",
                "has_files-2-id": "",
                "has_files-2-name": "",
                "has_files-2-file": "",
                "submit": "Update",
            },
        )

        # test
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, "/gmm/list/")
        assert_file_exists(self, "test.md")
        assert_file_not_exist(self, "test_image.png")

    def test_success_delete_gmm_view(self):
        # setup
        gmm, _ = get_test_gmm()
        url = f"/gmm/{gmm.pk}/delete"

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Are you sure you want to delete")

    def test_success_delete_gmm_action(self):
        # setup
        gmm, _ = get_test_gmm("I am a GMM", files=["delete_gmm.md", "delete_gmm.png"])
        url = f"/gmm/{gmm.pk}/delete"

        # act
        response = self.client.post(url)

        # test
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, "/gmm/list/")
        self.assertFalse(GMM.objects.filter(pk=gmm.pk).exists())
        assert_file_not_exist(self, "delete_gmm.md")
        assert_file_not_exist(self, "delete_gmm.png")


class GMMViewsTestMemberLoggedIn(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood"
        )
        Profile(
            user=self.user,
            nationality="Dutch",
            terms_confirmed=True,
            subscribed_newsletter=False,
        ).save()
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

    def test_success_list_empty(self):
        # setup
        url = "/gmm/list/"

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Switch view")
        self.assertNotContains(response, "Add new GMM")

    def test_denied_add(self):
        url = "/gmm/add/"
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)


class GMMViewsTestLoggedOut(TestCase):
    def setUp(self) -> None:
        self.client.logout()

    def test_success_list_empty(self):
        # setup
        url = "/gmm/list/"
        exp_message = "Please log in to see GMM information."

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(200, response.status_code)
        self.assertContains(response, exp_message)
        self.assertNotContains(response, "Switch view")
        self.assertNotContains(response, "Add new GMM")

    def test_denied_add(self):
        url = "/gmm/add/"
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)
