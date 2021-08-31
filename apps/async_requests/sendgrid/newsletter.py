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
from typing import List

from apps.async_requests.commands import SubscribeCommand, UnsubscribeCommand
from apps.users.models.user.profile import Profile


class NewsletterService(metaclass=ABCMeta):
    @abstractmethod
    def is_subscribed(self, email: str):
        """
        Checks subscription state of input email

        :param email: input email
        :return: True if email is subscribed to the newsletter
        """
        pass

    @abstractmethod
    def add_subscription(self, contacts):
        """
        Subscribes list of emails to the newsletter
        :param contacts: list of dictionaries which contain: email, first_name and last_name
        :return: True if all emails are subscribed successfully
        """
        pass

    @abstractmethod
    def remove_subscription(self, emails: List[str]):
        """
        Unsubscribe list of emails to the newsletter

        :param emails: list of emails to unsubscribe
        :return: True if all emails are unsubscribed successfully
        """
        pass

    @abstractmethod
    def send_mail(self, email):
        """
        Send emails via the sendgrid service
        
        :param email: sendgrid Mail object
        :return: True if email is sent succesfully
        """
        pass

    @staticmethod
    def sync_newsletter_preferences(profile: Profile):
        """
        Synchronizes newsletter preferences between Django server and newsletter backend.
        Does not check for previous state, hence may send redundant data eg. subscribe a user already subscribed

        :param profile: profile to sync preferences
        :return:
        """
        from apps.async_requests.factory import Factory

        service = Factory.get_newsletter_service()
        executor = Factory.get_executor()

        inst_email = profile.user.username
        alt_email = profile.user.email
        first_name = profile.user.first_name
        last_name = profile.user.last_name

        if not profile.subscribed_newsletter:
            # unsubscribe to both
            service.remove_subscription([inst_email, alt_email])
            return

        # Profile is subscribed to newsletter
        if profile.newsletter_recipient == "TUE":
            if not service.is_subscribed(inst_email):
                executor.add_command(SubscribeCommand(inst_email, first_name, last_name))
            executor.add_command(UnsubscribeCommand(alt_email))
        else:  # "ALT"
            if not service.is_subscribed(alt_email):
                executor.add_command(SubscribeCommand(alt_email, first_name, last_name))
            executor.add_command(UnsubscribeCommand(inst_email))

    @staticmethod
    def update_newsletter_preferences(profile: Profile, old_is_sub: bool, old_recipient: str, force=False):
        """
        Updates newsletter preferences

        :param profile:
        :param old_recipient:
        :param old_is_sub:
        :param force: force update to backend (optional)
        """
        # Subscribe user to newsletter when consented
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
