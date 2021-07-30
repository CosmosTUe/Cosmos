from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.models import Profile
from tests.helpers import assert_permission_denied


class GMMViewsTestAdminLoggedIn(TestCase):
    def setUp(self) -> None:
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

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
