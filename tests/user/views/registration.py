from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core import mail

from tests.user.views.wizard_helper import WizardViewTestCase


class RegistrationFlowTest(WizardViewTestCase):
    def assertEmailSent(self, recipient):
        exp_email_sender = "noreply@cosmostue.nl"
        exp_email_recipient = recipient
        exp_email_subject = "[Cosmos] Confirm your email address"

        self.assertEqual(len(mail.outbox), 1, "1 message sent")
        self.assertEqual(mail.outbox[0].to, exp_email_recipient)
        self.assertEqual(mail.outbox[0].from_email, exp_email_sender)
        self.assertEqual(mail.outbox[0].subject, exp_email_subject)
        self.assertWorkingActivationView()

    def assertNoEmailSent(self):
        self.assertEqual(len(mail.outbox), 0, "0 message sent")

    def assertWorkingActivationView(self):
        # setup
        html_parser = BeautifulSoup(mail.outbox[0].body, "html.parser")
        link = html_parser.find("a")
        link_text = link.contents.strip()
        link_url = link.get("href")

        exp_link_text = "Confirm your account registration"
        exp_activation_message = "Thank you for your email confirmation. Now you can login your account."

        # act
        response = self.client.get(link_url)

        # test
        self.assertEqual(link_text, exp_link_text)
        self.assertContains(response, exp_activation_message)

    def test_success_tue(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"
        exp_email_recipient = "tosti@student.tue.nl"

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
        self.assertEmailSent(exp_email_recipient)

    def test_success_fontys(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"
        exp_email_recipient = "tosti@fontys.nl"

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
        self.assertEmailSent(exp_email_recipient)

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
        self.assertNoEmailSent()

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
        self.assertNoEmailSent()

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
        self.assertNoEmailSent()
