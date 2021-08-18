from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.forms.auth import CosmosLoginForm
from apps.users.forms.errors import INVALID_EMAIL


def generate_form(username="tosti@student.tue.nl", password="ikbeeneenbrood", remember_me=False):
    data = {
        "username": username,
        "password": password,
    }
    if remember_me:
        data["remember_me"] = "on"
    return CosmosLoginForm(data=data)


def create_user(username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeeneenbrood"):
    user = User.objects.create_user(username=username, email=email, password=password)
    return user


class CosmosLoginFormTest(TestCase):
    def test_success_login_tue_email(self):
        # setup
        login_email = "tosti@student.tue.nl"
        create_user()

        # act
        form = generate_form(login_email)

        # test
        self.assertTrue(form.is_valid())

    def test_fail_personal_email_in_username(self):
        # setup
        login_email = "tosti@gmail.com"
        create_user()

        # act
        form = generate_form(login_email)

        # test
        self.assertTrue(form.has_error("username", INVALID_EMAIL))

    def test_fail_non_email_in_username(self):
        # setup
        login_email = "tosti.student"

        # act
        form = generate_form(login_email)

        self.assertTrue(form.has_error("username", INVALID_EMAIL))

    def test_fail_missing_email_in_db(self):
        # setup
        login_email = "mike@student.tue.nl"

        # act
        form = generate_form(login_email)

        # test
        self.assertFalse(form.has_error("username"))
        self.assertTrue(form.has_error("__all__", "invalid_login"))
