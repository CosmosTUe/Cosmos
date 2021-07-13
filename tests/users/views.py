from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase

# Test registration view
# Test update profile view
# Test update password view
# Test update preferences view
# Test update key access view
# Test delete view
# Test activate view


class UserViews(TestCase):
    def setUp(self) -> None:
        """
        Test successful registration via views for setup
        """
        response = self.client.post(
            "/accounts/register/",
            data={
                "username": "tosti@student.tue.nl",
                "email": "tosti@gmail.com",
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                "department": "Sustainable Innovation",
                "program": "Other",
                "terms_confirmed": True,
                "newsletter_recipient": "TUE",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

        new_user = User.objects.filter(username="tosti@student.tue.nl")
        self.assertTrue(new_user.exists())

    # TODO: reimplement this when errors are re-implemented in registration with bootstrap
    def test_fail_register_duplicate(self):
        """
        Test invalid register view when user already exists
        """
        # Ensure user still exists
        tosti_user = User.objects.filter(username="tosti@student.tue.nl")
        self.assertTrue(tosti_user.exists())

        # Create a logged out client
        c = Client()
        c.logout()

        # Attempt POST request
        response = c.post(
            "/accounts/register/",
            data={
                "username": "tosti@student.tue.nl",
                "email": "tosti@gmail.com",
                "first_name": "TostiFaker",
                "last_name": "BroodjesFaker",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                "department": "Sustainable Innovation",
                "program": "Other",
                "terms_confirmed": True,
                "newsletter_recipient": "TUE",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, "There is already a user with this email in our system, please try with a different one."
        )

    def test_fail_update_no_login(self):
        """
        Test invalid update view when logged out
        """
        # Ensure user still exists
        tosti_user = User.objects.filter(username="tosti@student.tue.nl")
        self.assertTrue(tosti_user.exists())

        # Create a logged out client
        c = Client()
        c.logout()

        # Attempt POST request
        response = c.post("/accounts/profile/")
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/accounts/login/?next=/accounts/profile/")

    def test_success_update_with_login(self):
        """
        Test valid update view when logged in
        """
        # Ensure user still exists
        tosti_user = User.objects.filter(username="tosti@student.tue.nl")
        self.assertTrue(tosti_user.exists())

        # Create logged in client
        c = Client()
        login_response = c.login(
            username="tosti@student.tue.nl",
            password="ikbeneenbrood",
        )
        self.assertTrue(login_response)

        # Attempt POST request
        response = c.post(
            "/accounts/profile/",
            data={
                "username": "tosti@student.tue.nl",
                "email": "tosti@gmail.com",
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "nationality": "German",
                "department": "Sustainable Innovation",
                "program": "Other",
                "newsletter_recipient": "TUE",
            },
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/")

    def test_fail_register_profile(self):
        """
        Test invalid register view when user already exists
        """

        # Create a logged out client
        c = Client()
        c.logout()

        # Attempt POST request
        c.post(
            "/accounts/register/",
            data={
                "username": "mike@student.tue.nl",
                "email": "tosti@gmail.com",
                "first_name": "TostiFaker",
                "last_name": "BroodjesFaker",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                "department": "",
                "program": "Other",
                "terms_confirmed": True,
                "newsletter_recipient": "TUE",
            },
        )

        mike_user = User.objects.filter(username="mike@student.tue.nl")
        self.assertFalse(mike_user.exists())
