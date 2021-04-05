from apps.async_requests.commands.command import Command


class MockCommand(Command):
    def __init__(self, can_merge, parameter):
        super(MockCommand, self).__init__(can_merge)
        self.parameters = [parameter]

    def merge(self, list_commands):
        for command in list_commands:
            self.parameters.extend(command.parameters)

    def execute(self):
        raise Exception("test")
