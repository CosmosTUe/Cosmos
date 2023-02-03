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

from newsletter.models import Newsletter, Subscription

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

        for newsletter, legacy_pref in newsletter_preferences:
            inst_sub, _ = Subscription.objects.get_or_create(newsletter=newsletter, email_field=inst_email)

            if pers_email is not None:
                pers_sub, _ = Subscription.objects.get_or_create(newsletter=newsletter, email_field=pers_email)
            else:
                pers_sub = None

            if not legacy_pref:
                # user unsubscribed from all newsletters
                inst_sub.update("unsubscribe")
                if pers_sub is not None:
                    pers_sub.update("unsubscribe")
            elif profile.newsletter_recipient == "TUE":
                inst_sub.update("subscribe")
                if pers_sub is not None:
                    pers_sub.update("unsubscribe")
            else:
                inst_sub.update("unsubscribe")
                if pers_sub is not None:
                    pers_sub.update("subscribe")
