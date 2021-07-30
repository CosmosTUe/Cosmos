from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.messages.storage.base import Message
from django.db import models
from django.test import Client
from django.urls import reverse

from apps.async_requests.factory import Factory

executor = Factory.get_executor()
newsletter_service = Factory.get_newsletter_service()


def assert_newsletter_subscription(test, email: str, state: bool):
    # setup - none

    # act
    executor.execute()

    # test
    test.assertEqual(state, newsletter_service.is_subscribed(email))


def assert_permission_denied(test, response):
    """Asserts 403 page is shown properly"""
    exp_message = "ERROR 403: Permission denied"
    test.assertEqual(200, response.status_code)
    test.assertContains(response, exp_message)


# Reference: https://stackoverflow.com/a/60323415/3787761
def get_admin_change_view_url(obj: models.Model) -> str:
    return reverse(f"admin:{obj._meta.app_label}_{type(obj).__name__.lower()}_change", args=(obj.pk,))


class BaseAdminTestCaseMixin:
    client: Client

    def setUp(self):
        self.client = Client()
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

    def get_instance(self):
        raise NotImplementedError()

    @staticmethod
    def get_messages(response) -> [Message]:
        return list(get_messages(response.wsgi_request))

    def test_change_view_loads_normally(self):
        instance = self.get_instance()
        response = self.client.get(get_admin_change_view_url(instance))
        self.assertEqual(200, response.status_code)
