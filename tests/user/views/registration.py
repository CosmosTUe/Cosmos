import smtplib
from unittest.mock import patch

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core import mail

from apps.async_requests.commands import MailSendCommand
from apps.async_requests.factory import Factory
from tests.user.views.wizard_helper import WizardViewTestCase

executor = Factory.get_executor()


class RegistrationFlowTest(WizardViewTestCase):
    def setUp(self) -> None:
        self.newsletter_service = Factory.get_newsletter_service(True)

    def assert_email_sent(self, recipient):
        # setup
        exp_email_sender = "noreply@cosmostue.nl"
        exp_email_recipient = recipient
        exp_email_subject = "[Cosmos] Confirm your email address"

        # act
        executor.execute()

        # test
        self.assertEqual(len(self.newsletter_service.outbox), 1, "1 message sent")
        self.assertEqual(self.newsletter_service.outbox[0].personalizations[0].tos[0]["email"], exp_email_recipient)
        self.assertEqual(self.newsletter_service.outbox[0].from_email.email, exp_email_sender)
        self.assertEqual(self.newsletter_service.outbox[0].subject.subject, exp_email_subject)
        self.assert_working_activation_view()

    def assert_no_email_sent(self):
        self.assertEqual(len(mail.outbox), 0, "0 message sent")

    def assert_working_activation_view(self):
        # setup
        html_parser = BeautifulSoup(self.newsletter_service.outbox[0].contents[0].content, "html.parser")
        link = html_parser.find("a")
        link_text = link.contents[0].strip()
        link_url = link.get("href")

        exp_link_text = "Confirm your account registration"
        exp_activation_message = "Thank you for your email confirmation. Now you can login your account."

        # act
        response = self.client.post(link_url)

        # test
        self.assertEqual(link_text, exp_link_text)
        self.assertContains(response, exp_activation_message)

    def assert_newsletter_subscription(self, email: str, state: bool):
        # setup - none

        # act
        executor.execute()

        # test
        self.assertEqual(state, self.newsletter_service.is_subscribed(email))

    def test_success_tue_without_newsletter(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"
        exp_email_recipient = "tosti@student.tue.nl"

        inst_email = "tosti@student.tue.nl"
        inst_sub = False
        alt_email = "tosti@gmail.com"
        alt_sub = False

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
                },
                "register_tue": {
                    "department": "Mathematics and Computer Science",
                    "program": "Bachelor",
                },
            },
        )

        # test
        self.assertEqual(done_url, response.url)
        self.assert_email_sent(exp_email_recipient)
        self.assert_newsletter_subscription(inst_email, inst_sub)
        self.assert_newsletter_subscription(alt_email, alt_sub)

    def test_success_tue_with_newsletter(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"
        exp_email_recipient = "tosti@student.tue.nl"

        inst_email = "tosti@student.tue.nl"
        inst_sub = True
        alt_email = "tosti@gmail.com"
        alt_sub = False

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
        self.assert_email_sent(exp_email_recipient)
        self.assert_newsletter_subscription(inst_email, inst_sub)
        self.assert_newsletter_subscription(alt_email, alt_sub)

    # def test_success_fontys(self):
    #     # setup
    #     url = "/accounts/register/"
    #     done_url = "/accounts/register/done/"
    #     exp_email_recipient = "tosti@fontys.nl"

    #     # act
    #     response = self.get_wizard_response(
    #         url,
    #         {
    #             "register_user": {
    #                 "first_name": "Tosti",
    #                 "last_name": "Broodjes",
    #                 "username": "tosti@fontys.nl",
    #                 "email": "tosti@gmail.com",
    #                 "password1": "ikbeneenbrood",
    #                 "password2": "ikbeneenbrood",
    #                 "nationality": "Dutch",
    #                 "terms_confirmed": "on",
    #                 "subscribed_newsletter": "on",
    #             },
    #             "register_fontys": {
    #                 "study": "test",  # TODO fix Fontys studies
    #             },
    #         },
    #     )

    #     # test
    #     self.assertEqual(done_url, response.url)
    #     self.assert_email_sent(exp_email_recipient)

    def test_fail_terms_unchecked(self):
        # setup
        url = "/accounts/register/"
        wizard_name = "registration_wizard"
        step = "register_user"
        exp_error_msg = "This field is required"

        # act
        response = self.get_wizard_step_response(
            url,
            wizard_name,
            step,
            {
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "username": "tosti@student.tue.nl",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
                "nationality": "Dutch",
                # "terms_confirmed": "off",
                "subscribed_newsletter": "on",
            },
        )

        # test
        self.assertTrue(self.wizard_has_validation_error(response))
        self.assertContains(response, exp_error_msg)
        self.assert_no_email_sent()

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
        self.assert_no_email_sent()

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
        self.assert_no_email_sent()

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
        self.assert_no_email_sent()

    def test_fail_invalid_token_authentication(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"

        inst_email = "tosti@student.tue.nl"
        inst_sub = False
        alt_email = "tosti@gmail.com"
        alt_sub = False

        # act
        with patch.object(MailSendCommand, "execute") as mock_method:
            mock_method.side_effect = smtplib.SMTPServerDisconnected()
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
                    },
                    "register_tue": {
                        "department": "Mathematics and Computer Science",
                        "program": "Bachelor",
                    },
                },
            )

        # test
        self.assertEqual(done_url, response.url)
        self.assert_no_email_sent()
        self.assert_newsletter_subscription(inst_email, inst_sub)
        self.assert_newsletter_subscription(alt_email, alt_sub)
