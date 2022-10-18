from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.base import Message
from django.db import models
from django.test import Client
from django.urls import reverse
from newsletter.models import Newsletter, Subscription

from apps.async_requests.factory import Factory
from apps.async_requests.newsletter.newsletter_service import NewsletterService


# Reference: https://stackoverflow.com/a/60323415/3787761
def get_admin_change_view_url(obj: models.Model) -> str:
    return reverse(f"admin:{obj._meta.app_label}_{type(obj).__name__.lower()}_change", args=(obj.pk,))


class NewsletterTestCaseMixin:
    newsletter_service: NewsletterService

    def setUp(self):
        # TODO adapt to django-newsletter
        self.newsletter_service = Factory.get_newsletter_service(True)
        self.news = Newsletter.objects.create(
            title="Cosmos News", slug="cosmos-news", email="noreply@cosmostue.nl", sender="Cosmos"
        )
        self.gmm = Newsletter.objects.create(
            title="GMM", slug="gmm", email="noreply@cosmostue.nl", sender="Cosmos Board"
        )
        return super(NewsletterTestCaseMixin, self).setUp()

    def tearDown(self) -> None:
        Subscription.objects.all().delete()

    @staticmethod
    def _set_subscription(newsletter: Newsletter, email: str, state: bool):
        sub = Subscription.objects.create(newsletter=newsletter, email_field=email)
        if state:
            sub.update("subscribe")
        else:
            sub.update("unsubscribe")

    def set_newsletter_subscription(self, email: str, state: bool):
        self._set_subscription(self.news, email, state)

    def set_gmm_invite_subscription(self, email: str, state: bool):
        self._set_subscription(self.gmm, email, state)

    def _assert_subscription(self, newsletter: Newsletter, email: str, state: bool):
        subs = Subscription.objects.filter(newsletter=newsletter, email_field=email)
        if subs.exists():
            self.assertEqual(subs[0].subscribed, state)
        else:
            self.assertFalse(state, f'{email} should have no subscription to "{newsletter.title}"')

    def assert_newsletter_subscription(self, email: str, state: bool):
        self._assert_subscription(self.news, email, state)

    def assert_gmm_invite_subscription(self, email: str, state: bool):
        self._assert_subscription(self.gmm, email, state)


# noinspection PyUnresolvedReferences
class BaseAdminTestCaseMixin:
    client: Client

    def setUp(self):
        self.client = Client()
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")
        return super(BaseAdminTestCaseMixin, self).setUp()

    def get_instance(self):
        raise NotImplementedError()

    @staticmethod
    def get_messages(response) -> [Message]:
        return list(get_messages(response.wsgi_request))

    def test_change_view_loads_normally(self):
        instance = self.get_instance()
        response = self.client.get(get_admin_change_view_url(instance))
        self.assertEqual(200, response.status_code)


def get_profile_form_data(
    first_name="Tosti",
    last_name="Broodjes",
    username="tosti@student.tue.nl",
    email="tosti@gmail.com",
    nationality="Dutch",
    department="Electrical Engineering",
    program="Bachelor",
    study="",
):
    output = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "nationality": nationality,
        "department": department,
        "program": program,
        "study": study,
        "save_profile": "Submit",
    }
    return {k: v for k, v in output.items() if v is not None}


def get_preferences_form_data(news="NONE", gmm="NONE"):
    output = {
        "save_preferences": "Submit",
        "newsletter-cosmos-news": news,
        "newsletter-gmm": gmm,
    }

    return output
