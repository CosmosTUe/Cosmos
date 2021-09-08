from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import TestCase


class LoginViewTest(TestCase):
    def test_correct_field_labels(self):
        # setup
        url = "/accounts/login/"

        # act
        response = self.client.get(url)

        # test
        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        labels = html_parser.find_all("label")
        self.assertEqual(labels[0].text.strip(), "Institutional Email")
        self.assertEqual(labels[1].text.strip(), "Password")
        self.assertEqual(labels[2].text.strip(), "Remember me")

    def test_fail_login_inactive_user(self):
        # setup
        User.objects.create_user(
            username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood", is_active=False
        )
        url = "/accounts/login/"
        exp_message = "Please enter a correct username and password. Note that both fields may be case-sensitive."

        # act
        response = self.client.post(url, data={"username": "tosti@student.tue.nl", "password": "ikbeneenbrood"})

        # test
        self.assertEqual(200, response.status_code)
        self.assertEqual("/accounts/login/", response.wsgi_request.path)
        self.assertContains(response, exp_message)

    def test_pass_login_active_user(self):
        # setup
        User.objects.create_user(
            username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood", is_active=True
        )
        url = "/accounts/login/"

        # act
        response = self.client.post(url, data={"username": "tosti@student.tue.nl", "password": "ikbeneenbrood"})

        # test
        self.assertEqual(302, response.status_code)
        self.assertEqual("/accounts/profile/", response.url)
        pass
