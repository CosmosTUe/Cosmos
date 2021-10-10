import jsonpickle
from django.test import TestCase
from sendgrid.helpers.mail.mail import Mail

from apps.async_requests.commands import MailSendCommand, SubscribeCommand, UnsubscribeCommand


class CommandsTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        super().tearDown()

    def test_merge_mailsendcommand(self):
        email1 = Mail(subject="test", html_content="Body", from_email="test@example.com")
        email2 = Mail(subject="test2", html_content="Body2", from_email="test2@example.com")
        command1 = MailSendCommand(email1)
        command2 = MailSendCommand(email2)
        command1.merge([command2])
        self.assertTrue(len(command1.emails) == 2)
        self.assertTrue(command1.emails[0] == email1)
        self.assertTrue(command1.emails[1] == email2)

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

    def test_serialize_mailsendcommand(self):
        command = MailSendCommand(Mail(subject="test", html_content="Body", from_email="test@example.com"))
        pickle = jsonpickle.encode(command)
        result = jsonpickle.decode(pickle)

        self.assertTrue(command == result)

    def test_serialize_subscribecommand(self):
        command = SubscribeCommand("test@example.com", "Mike", "Wazowski")
        pickle = jsonpickle.encode(command)
        result = jsonpickle.decode(pickle)

        self.assertTrue(command == result)

    def test_serialize_unsubsribecomand(self):
        command = UnsubscribeCommand("test@example.com")
        pickle = jsonpickle.encode(command)
        result = jsonpickle.decode(pickle)

        self.assertTrue(command == result)
