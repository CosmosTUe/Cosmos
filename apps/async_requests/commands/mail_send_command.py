from django.core import mail

from apps.async_requests.commands.command import Command


class MailSendCommand(Command):
    def __init__(self, email):
        super(MailSendCommand, self).__init__(True)
        self.emails = [email]

    def merge(self, list_commands):
        for command in list_commands:
            self.emails.extend(command.emails)

    def execute(self):
        connection = mail.get_connection()
        connection.send_messages(self.emails)
