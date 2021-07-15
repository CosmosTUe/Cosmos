from apps.async_requests.commands.command import Command


class UnsubscribeCommand(Command):
    def __init__(self, email):
        super(UnsubscribeCommand, self).__init__(True)
        self.emails = [email]

    def merge(self, list_commands):
        for command in list_commands:
            self.emails.extend(command.emails)

    def execute(self):
        from apps.async_requests.factory import Factory

        newsletter_service = Factory.get_newsletter_service()
        newsletter_service.remove_subscription(self.emails)

    def __eq__(self, other):
        return super().__eq__(other) and self.emails == other.emails
