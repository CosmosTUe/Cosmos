from abc import abstractmethod

from apps.async_requests.commands.command import Command
from apps.async_requests.constants import NEWSLETTER_LIST_ID, GMM_INVITE_LIST_ID


class SubscribeCommand(Command):
    @property
    @abstractmethod
    def list_id(self) -> str:
        return ""

    def __init__(self, email, first_name, last_name):
        super(SubscribeCommand, self).__init__(True)
        self.contacts = [{"email": email, "first_name": first_name, "last_name": last_name}]

    def merge(self, list_commands):
        for command in list_commands:
            self.contacts.extend(command.contacts)

    def execute(self):
        from apps.async_requests.factory import Factory

        newsletter_service = Factory.get_newsletter_service()
        newsletter_service.add_subscription(self.contacts, self.list_id)

    def __eq__(self, other):
        return super().__eq__(other) and self.contacts == other.contacts


class NewsletterSubscribeCommand(SubscribeCommand):
    def __init__(self, email, first_name, last_name):
        super(NewsletterSubscribeCommand, self).__init__(email, first_name, last_name)

    @property
    def list_id(self) -> str:
        return NEWSLETTER_LIST_ID


class GMMInviteSubscribeCommand(SubscribeCommand):
    def __init__(self, email, first_name, last_name):
        super(GMMInviteSubscribeCommand, self).__init__(email, first_name, last_name)

    @property
    def list_id(self) -> str:
        return GMM_INVITE_LIST_ID
