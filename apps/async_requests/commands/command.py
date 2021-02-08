class Command():

    def __init__(self, can_merge, backoff_factor=2):
        self.can_merge = can_merge
        self.timer = 0
        self.times_delayed = 0
        self.backoff_factor = backoff_factor

    def can_merge(self):
        return self.can_merge

    def merge(self, list_commands):
        pass

    def execute(self):
        pass
