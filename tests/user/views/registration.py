from django.contrib.auth.models import User

from tests.user.views.wizard_helper import WizardViewTestCase


class RegistrationViewTest(WizardViewTestCase):
    def test_success_tue(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"

        # act
        response = self.get_wizard_response(
            url,
            {
                "register_user": {
                    "first_name": "Tosti",
                    "last_name": "Broodjes",
                    "username": "tosti@student.tue.nl",
                    "email": "tosti@gmail.com",
                    "password1": "ikbeneenbrood",
                    "password2": "ikbeneenbrood",
                    "nationality": "Dutch",
                    "terms_confirmed": "on",
                    "subscribed_newsletter": "on",
                },
                "register_tue": {
                    "department": "Mathematics and Computer Science",
                    "program": "Bachelor",
                },
            },
        )

        # test
        self.assertEqual(done_url, response.url)

    def test_success_fontys(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"

        # act
        response = self.get_wizard_response(
            url,
            {
                "register_user": {
                    "first_name": "Tosti",
                    "last_name": "Broodjes",
                    "username": "tosti@fontys.nl",
                    "email": "tosti@gmail.com",
                    "password1": "ikbeneenbrood",
                    "password2": "ikbeneenbrood",
                    "nationality": "Dutch",
                    "terms_confirmed": "on",
                    "subscribed_newsletter": "on",
                },
                "register_fontys": {
                    "study": "test",  # TODO fix Fontys studies
                },
            },
        )

        # test
        self.assertEqual(done_url, response.url)

    def test_fail_register_duplicate(self):
        """
        Test invalid register view when user already exists
        """
        # setup
        url = "/accounts/register/"
        wizard_name = "registration_wizard"
        step = "register_user"
        exp_error_msg = "A user with that username already exists"

        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood")

        # act
        response = self.get_wizard_step_response(
            url,
            wizard_name,
            step,
            {
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "username": "tosti@student.tue.nl",
                "email": "tosti@gmail.com",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                "terms_confirmed": "on",
                "subscribed_newsletter": "on",
            },
        )

        # test
        self.assertTrue(self.wizard_has_validation_error(response))
        self.assertContains(response, exp_error_msg)

    def test_fail_register_username_gmail(self):
        """
        User registration fails when non-institution email is given as username
        """
        # setup
        url = "/accounts/register/"
        wizard_name = "registration_wizard"
        step = "register_user"
        exp_error_msg = "Please enter your institutional email"

        # act
        response = self.get_wizard_step_response(
            url,
            wizard_name,
            step,
            {
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "username": "tosti@gmail.com",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                "terms_confirmed": "on",
                "subscribed_newsletter": "on",
            },
        )

        # test
        self.assertTrue(self.wizard_has_validation_error(response))
        self.assertContains(response, exp_error_msg)

    def test_fail_register_username_fake_tue(self):
        """
        User registration fails when non-institution email is given as username
        """
        # setup
        url = "/accounts/register/"
        wizard_name = "registration_wizard"
        step = "register_user"
        exp_error_msg = "Please enter your institutional email"

        # act
        response = self.get_wizard_step_response(
            url,
            wizard_name,
            step,
            {
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "username": "tosti@cosmostue.com",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                "terms_confirmed": "on",
                "subscribed_newsletter": "on",
            },
        )

        # test
        self.assertTrue(self.wizard_has_validation_error(response))
        self.assertContains(response, exp_error_msg)
