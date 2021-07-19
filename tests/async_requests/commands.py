from unittest import TestCase

from django.core.mail import EmailMessage

from apps.async_requests.commands import MailSendCommand, SubscribeCommand, UnsubscribeCommand


class CommandsTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        super().tearDown()

    def test_merge_mailsendcommand(self):
        command1 = MailSendCommand(EmailMessage("test", "Body", from_email="test@example.com"))
        command2 = MailSendCommand(EmailMessage("test2", "Body2", from_email="test2@example.com"))
        command1.merge([command2])
        self.assertTrue(len(command1.emails) == 2)
        self.assertTrue(
            command1.emails[0].__dict__ == EmailMessage("test", "Body", from_email="test@example.com").__dict__
        )
        self.assertTrue(
            command1.emails[1].__dict__ == EmailMessage("test2", "Body2", from_email="test2@example.com").__dict__
        )

    def test_merge_subscribecommand(self):
        command1 = SubscribeCommand("test@example.com", "Mike", "Wazowski")
        command2 = SubscribeCommand("test2@example.com", "James", "Sullivan")
        command1.merge([command2])
        self.assertTrue(len(command1.contacts) == 2)
        self.assertTrue(
            command1.contacts[0] == {"email": "test@example.com", "first_name": "Mike", "last_name": "Wazowski"}
        )
        self.assertTrue(
            command1.contacts[1] == {"email": "test2@example.com", "first_name": "James", "last_name": "Sullivan"}
        )

    def test_merge_unsubscribecommand(self):
        command1 = UnsubscribeCommand("test@example.com")
        command2 = UnsubscribeCommand("test2@example.com")
        command1.merge([command2])
        self.assertTrue(len(command1.emails) == 2)
        self.assertTrue(command1.emails[0] == "test@example.com")
        self.assertTrue(command1.emails[1] == "test2@example.com")
