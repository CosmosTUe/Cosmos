import os

from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.forms import errors
from apps.users.models import Profile
from tests.helpers import assert_permission_denied


def assert_file_exists(test: TestCase, file_name):
    url = f"/media/gmm/{file_name}"
    response = test.client.get(url)
    test.assertEqual(200, response.status_code)


def get_new_file(name):
    if not os.path.exists("temp/"):
        os.mkdir("temp")
    with open(f"temp/{name}", "w") as test:
        test.write(" ")
    return open(f"temp/{name}", "rb")


def clear_temp_files():
    for filename in os.listdir("temp/"):
        os.remove(f"temp/{filename}")
    os.removedirs("temp/")


class GMMViewsTestAdminLoggedIn(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

    @classmethod
    def tearDownClass(cls):
        clear_temp_files()

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
        self.assertTrue(form.has_error("name", errors.REQUIRED))
        self.assertTrue(form.has_error("date", errors.REQUIRED))

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
        self.assertRedirects(response, "/resources/")

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
                    "has_files-0-name": "file name",
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
                    "has_files-TOTAL_FORMS": 1,
                    "has_files-INITIAL_FORMS": 0,
                    "has_files-MIN_NUM_FORMS": 0,
                    "has_files-MAX_NUM_FORMS": 1000,
                    "has_files-0-id": "",
                    "has_files-0-name": "file name",
                    "has_files-0-file": md,
                    "has_files-1-id": "",
                    "has_files-1-name": "image",
                    "has_files-1-file": img,
                    "submit": "Create",
                },
            )

        # test
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, "/gmm/list/")
        assert_file_exists(self, "test.md")
        assert_file_exists(self, "img.png")


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
        assert_permission_denied(self, response)


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
        assert_permission_denied(self, response)
