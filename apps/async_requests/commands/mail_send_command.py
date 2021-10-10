from sendgrid.helpers.mail import Mail

from apps.async_requests.commands.command import Command


class MailSendCommand(Command):
    def __init__(self, email: Mail):
        super(MailSendCommand, self).__init__(True)
        self.emails = [email]

    def merge(self, list_commands):
        for command in list_commands:
            self.emails.extend(command.emails)

    def execute(self):
        from apps.async_requests.factory import Factory

        for email in self.emails:
            Factory.get_newsletter_service().send_mail(email)

    def __eq__(self, other):
        return super().__eq__(other) and self.emails == self.emails
