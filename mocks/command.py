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

    def __eq__(self, other):
        return super().__eq__(other) and self.parameters == other.parameters

    # def __repr__(self):
    #     return f"<{self.__class__.__name__} {self.parameters}>"


class SecondMockCommand(MockCommand):
    pass
