"""
COSMOS uses SendGrid to handle newsletters.

NOTE:
Use the API documentation linked below.
The one linked in `newsletter/newsletter-python` is for legacy and not to be used.

References:
https://github.com/sendgrid/sendgrid-python
https://github.com/sendgrid/python-http-client
https://sendgrid.api-docs.io/v3.0/how-to-use-the-sendgrid-v3-api/api-authentication
"""
from abc import ABCMeta, abstractmethod
from typing import List

from newsletter.models import Subscription, Newsletter

from apps.async_requests.commands import (
    GMMInviteSubscribeCommand,
    GMMInviteUnsubscribeCommand,
    NewsletterSubscribeCommand,
    NewsletterUnsubscribeCommand,
)
from apps.async_requests.constants import GMM_INVITE_LIST_ID, NEWSLETTER_LIST_ID
from apps.users.models.profile import Profile

SUBSCRIPTIONS = [
    ("subscribed_newsletter", NEWSLETTER_LIST_ID, NewsletterSubscribeCommand, NewsletterUnsubscribeCommand),
    ("subscribed_gmm_invite", GMM_INVITE_LIST_ID, GMMInviteSubscribeCommand, GMMInviteUnsubscribeCommand),
]


class NewsletterService(metaclass=ABCMeta):
    @abstractmethod
    def is_subscribed(self, email: str, list_id: str):
        """
        Checks subscription state of input email

        :param email: input email
        :param list_id: list ID
        :return: True if email is subscribed to the newsletter
        """
        pass

    @abstractmethod
    def add_subscription(self, contacts: List, list_id: str):
        """
        Subscribes list of emails to the newsletter
        :param contacts: list of dictionaries which contain: email, first_name and last_name
        :param list_id: list ID
        :return: True if all emails are subscribed successfully
        """
        pass

    @abstractmethod
    def remove_subscription(self, emails: List[str], list_id: str):
        """
        Unsubscribe list of emails to the newsletter

        :param emails: list of emails to unsubscribe
        :param list_id: list ID
        :return: True if all emails are unsubscribed successfully
        """
        pass

    @abstractmethod
    def remove_contacts(self, emails):
        """
        Remove contact emails from database

        :param emails:
        :return: True if all emails are removed successfully
        """
        pass

    @abstractmethod
    def send_mail(self, email):
        """
        Send emails via the newsletter service

        :param email: newsletter Mail object
        :return: True if email is sent succesfully
        """
        pass

    def sync_subscription_preferences(self, profile: Profile):
        """
        Synchronizes newsletter preferences between Django server and newsletter backend.
        Does not check for previous state, hence may send redundant data eg. subscribe a user already subscribed

        :param profile: profile to sync preferences
        :return:
        """
        inst_email = profile.user.username
        pers_email = profile.user.email

        newsletter_preferences = [
            (Newsletter.objects.get(slug__exact="cosmos-news"), profile.subscribed_newsletter),
            (Newsletter.objects.get(slug__exact="gmm"), profile.subscribed_gmm_invite),
        ]

        for (newsletter, legacy_pref) in newsletter_preferences:
            inst_sub, _ = Subscription.objects.get_or_create(newsletter=newsletter, email_field=inst_email)
            pers_sub, _ = Subscription.objects.get_or_create(newsletter=newsletter, email_field=pers_email)
            if not legacy_pref:
                # user unsubscribed from all newsletters
                inst_sub.update("unsubscribe")
                pers_sub.update("unsubscribe")
            elif profile.newsletter_recipient == "TUE":
                inst_sub.update("subscribe")
                pers_sub.update("unsubscribe")
            else:
                inst_sub.update("unsubscribe")
                pers_sub.update("subscribe")

    @staticmethod
    def update_newsletter_preferences(profile: Profile, initial_data: dict, new_data: dict):
        """
        Updates newsletter preferences

        :param profile:
        :param new_data:
        :param initial_data:
        """
        # Subscribe user to newsletter when consented
        from apps.async_requests.factory import Factory

        executor = Factory.get_executor()

        # skip if no changes detected
        if initial_data == new_data:
            return

        first_name = profile.user.first_name
        last_name = profile.user.last_name

        # get old and new emails
        if initial_data["newsletter_recipient"] == "TUE":
            old_email = profile.user.username
        else:
            old_email = profile.user.email

        if new_data["newsletter_recipient"] == "TUE":
            new_email = profile.user.username
        else:
            new_email = profile.user.email

        # detect recipient change
        if initial_data["newsletter_recipient"] != new_data["newsletter_recipient"]:
            # unsub old
            if initial_data["subscribed_newsletter"]:
                executor.add_command(NewsletterUnsubscribeCommand(old_email))
            if initial_data["subscribed_gmm_invite"]:
                executor.add_command(GMMInviteUnsubscribeCommand(old_email))

            # sub new
            if new_data["subscribed_newsletter"]:
                executor.add_command(NewsletterSubscribeCommand(new_email, first_name, last_name))
            if new_data["subscribed_gmm_invite"]:
                executor.add_command(GMMInviteSubscribeCommand(new_email, first_name, last_name))

            return

        # assumes same email
        # detect state change (XOR)
        if initial_data["subscribed_newsletter"] ^ new_data["subscribed_newsletter"]:
            if initial_data["subscribed_newsletter"]:
                # unsubscribing
                executor.add_command(NewsletterUnsubscribeCommand(old_email))
            else:
                # subscribing
                executor.add_command(NewsletterSubscribeCommand(new_email, first_name, last_name))

        if initial_data["subscribed_gmm_invite"] ^ new_data["subscribed_gmm_invite"]:
            if initial_data["subscribed_gmm_invite"]:
                # unsubscribing
                executor.add_command(GMMInviteUnsubscribeCommand(old_email))
            else:
                # subscribing
                executor.add_command(GMMInviteSubscribeCommand(new_email, first_name, last_name))
