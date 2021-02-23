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

from apps.users.models.user.profile import Profile, state_prefix


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

    def update_newsletter_preferences(self, profile: Profile, force=False):
        """
        Updates newsletter preferences

        :param profile: profile to change preferences
        :param force: force update to backend (optional)
        """
        # Subscribe user to newsletter when consented

        from apps.async_requests.commands.subscribe_command import SubscribeCommand
        from apps.async_requests.commands.unsubscribe_command import UnsubscribeCommand
        from apps.async_requests.factory import Factory

        executor = Factory.get_executor()

        # extract attributes
        old_is_sub = getattr(profile, f"{state_prefix}subscribed_newsletter")
        old_recipient = getattr(profile, f"{state_prefix}newsletter_recipient")

        is_sub = getattr(profile, "subscribed_newsletter")
        recipient = getattr(profile, "newsletter_recipient")

        # skip if no changes detected
        if not force and old_is_sub == is_sub and old_recipient == recipient:
            return

        # handle old email first
        if old_is_sub:
            # unsubscribe old email
            if old_recipient == "TUE":
                executor.add_command(UnsubscribeCommand(profile.user.username))
            else:
                executor.add_command(UnsubscribeCommand(profile.user.email))

        # handle new email next
        if is_sub:
            # subscribe new email
            if recipient == "TUE":
                email = profile.user.username
            else:
                email = profile.user.email
            executor.add_command(SubscribeCommand(email, profile.user.first_name, profile.user.last_name))
