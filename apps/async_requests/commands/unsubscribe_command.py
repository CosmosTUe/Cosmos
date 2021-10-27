from abc import abstractmethod

from apps.async_requests.commands.command import Command
from apps.async_requests.constants import NEWSLETTER_LIST_ID, GMM_INVITE_LIST_ID


class UnsubscribeCommand(Command):
    @property
    @abstractmethod
    def list_id(self) -> str:
        return ""

    def __init__(self, email):
        super(UnsubscribeCommand, self).__init__(True)
        self.emails = [email]

    def merge(self, list_commands):
        for command in list_commands:
            self.emails.extend(command.emails)

    def execute(self):
        from apps.async_requests.factory import Factory

        newsletter_service = Factory.get_newsletter_service()
        newsletter_service.remove_subscription(self.emails, self.list_id)

    def __eq__(self, other):
        return super().__eq__(other) and self.emails == other.emails


class NewsletterUnsubscribeCommand(UnsubscribeCommand):
    @property
    def list_id(self) -> str:
        return NEWSLETTER_LIST_ID


class GMMInviteUnsubscribeCommand(UnsubscribeCommand):
    @property
    def list_id(self) -> str:
        return GMM_INVITE_LIST_ID
