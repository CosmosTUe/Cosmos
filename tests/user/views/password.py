from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from apps.async_requests.factory import Factory

executor = Factory.get_executor()


class PasswordResetViewTest(TestCase):
    def assert_email_sent(self, recipient):
        # setup
        exp_email_sender = "noreply@cosmostue.nl"
        exp_email_recipient = recipient
        exp_email_subject = "[Cosmos] Password reset"

        # act
        executor.execute()

        # test
        self.assertEqual(len(mail.outbox), 1, "1 message sent")
        self.assertEqual(mail.outbox[0].to[0], exp_email_recipient)
        self.assertEqual(mail.outbox[0].from_email, exp_email_sender)
        self.assertEqual(mail.outbox[0].subject, exp_email_subject)

    def test_success(self):
        # setup
        User.objects.create_user(
            username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood"
        ).save()
        url = "/accounts/password_reset/"

        exp_status_code = 302
        exp_url = "/accounts/password_reset/done/"

        # act
        response = self.client.post(
            url,
            {
                "email": "tosti@student.tue.nl",
                "submit": "Reset+password",
            },
        )

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_url, response.url)
        self.assert_email_sent("tosti@student.tue.nl")
