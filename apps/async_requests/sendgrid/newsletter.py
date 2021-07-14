"""
COSMOS uses SendGrid to handle newsletters.

NOTE:
Use the API documentation linked below.
The one linked in `sendgrid/sendgrid-python` is for legacy and not to be used.

References:
https://github.com/sendgrid/sendgrid-python
https://github.com/sendgrid/python-http-client
https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-authentication
"""
from abc import ABCMeta, abstractmethod

from apps.users.models.user.profile import Profile


class NewsletterService(metaclass=ABCMeta):
    @abstractmethod
    def is_subscribed(self, email: str):
        pass

    @abstractmethod
    def add_subscription(self, contacts):
        pass

    @abstractmethod
    def remove_subscription(self, emails):
        pass

    def sync_newsletter_preferences(self, profile: Profile):
        """
        Synchronizes newsletter preferences between Django server and newsletter backend.
        Does not check for previous state, hence may send redundant data eg. subscribe a user already subscribed

        :param profile: profile to sync preferences
        :return:
        """
        from apps.async_requests.factory import Factory

        # TODO
        if profile.newsletter_recipient == "TUE":
            pass
        executor = Factory.get_executor()
        executor.execute()

    def update_newsletter_preferences(self, profile: Profile, old_is_sub: bool, old_recipient: str, force=False):
        """
        Updates newsletter preferences

        :param profile:
        :param old_recipient:
        :param old_is_sub:
        :param force: force update to backend (optional)
        """
        # Subscribe user to newsletter when consented
        from apps.async_requests.commands.subscribe_command import SubscribeCommand
        from apps.async_requests.commands.unsubscribe_command import UnsubscribeCommand
        from apps.async_requests.factory import Factory

        executor = Factory.get_executor()

        # extract attributes
        new_is_sub = profile.subscribed_newsletter
        new_recipient = profile.newsletter_recipient

        # skip if no changes detected
        if not force and old_is_sub == new_is_sub and old_recipient == new_recipient:
            return

        # handle old email first
        if old_is_sub:
            # unsubscribe old email
            if old_recipient == "TUE":
                executor.add_command(UnsubscribeCommand(profile.user.username))
            else:
                executor.add_command(UnsubscribeCommand(profile.user.email))

        # handle new email next
        if new_is_sub:
            # subscribe new email
            if new_recipient == "TUE":
                email = profile.user.username
            else:
                email = profile.user.email
            executor.add_command(SubscribeCommand(email, profile.user.first_name, profile.user.last_name))
