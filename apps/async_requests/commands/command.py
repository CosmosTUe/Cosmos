from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, can_merge, backoff_factor=2):
        self.can_merge = can_merge
        self.timer = 0
        self.times_delayed = 0
        self.backoff_factor = backoff_factor

    def get_can_merge(self):
        return self.can_merge

    @abstractmethod
    def merge(self, list_commands):
        pass

    @abstractmethod
    def execute(self):
        pass

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.can_merge == other.can_merge
            and self.timer == other.timer
            and self.times_delayed == other.times_delayed
            and self.backoff_factor == other.backoff_factor
        )
