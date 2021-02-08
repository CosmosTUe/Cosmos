from apps.async_requests.commands.command import Command


class SubscriptionCommand(Command):
    def __init__(self, email, first_name, last_name):
        super.__init__(self, True)
        self.contacts = [{"email": email, "first_name": first_name, "last_name": last_name}]

    def merge(self, list_commands):
        for command in list_commands:
            self.contacts.extend(command.contacts)

    def execute(self):
        pass
