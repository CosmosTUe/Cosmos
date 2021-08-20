from http.client import HTTPException
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from python_http_client import UnauthorizedError

from apps.async_requests.sendgrid.newsletter import NewsletterService
from apps.users.models import Profile
from tests.helpers import BaseAdminTestCaseMixin, NewsletterTestCaseMixin


class ProfileAdminViewTest(BaseAdminTestCaseMixin, NewsletterTestCaseMixin, TestCase):
    def setUp(self):
        super().setUp()

    def get_instance(self):
        user = User.objects.create_user(
            username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood"
        )
        instance, _ = Profile.objects.get_or_create(
            user=user,
            nationality="Dutch",
            terms_confirmed=True,
            subscribed_newsletter=False,
        )
        return instance

    def assert_changes_informed_to_user(self, response, change_count):
        exp_message_count = 2
        exp_loading_msg = f"Sending {change_count} messages..."
        exp_ending_msg = f"{change_count} newsletter preferences updated!"

        messages = self.get_messages(response)

        self.assertEqual(exp_message_count, len(messages))
        self.assertEqual(exp_loading_msg, str(messages[0]))
        self.assertEqual(exp_ending_msg, str(messages[1]))

    def assert_error_informed_to_user(self, response, change_count, error_msg):
        exp_message_count = 2
        exp_loading_msg = f"Sending {change_count} messages..."
        messages = self.get_messages(response)

        self.assertEqual(exp_message_count, len(messages))
        self.assertEqual(exp_loading_msg, str(messages[0]))
        self.assertEqual(error_msg, str(messages[1]))
        self.assertEqual("error", messages[1].level_tag)

    def test_sync_newsletter_subscriptions_no_changes(self):
        # setup
        create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=False)
        create_new_profile(first_name="B", username="b@student.tue.nl", newsletter=False)
        create_new_profile(first_name="C", username="c@student.tue.nl", newsletter=False)
        url = "/admin/users/profile/"

        exp_status_code = 302
        exp_change_count = 3

        # act
        response = self.client.post(
            url,
            data={
                "action": "sync_newsletter_subscriptions",
                "_selected_action": [
                    get_profile("a@student.tue.nl").pk,
                    get_profile("b@student.tue.nl").pk,
                    get_profile("c@student.tue.nl").pk,
                ],
            },
        )

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assert_changes_informed_to_user(response, exp_change_count)
        self.assert_newsletter_subscription("a@student.tue.nl", False)
        self.assert_newsletter_subscription("b@student.tue.nl", False)
        self.assert_newsletter_subscription("c@student.tue.nl", False)

    def test_sync_newsletter_subscriptions_one_new_subscription(self):
        # setup
        create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=True)
        create_new_profile(first_name="B", username="b@student.tue.nl", newsletter=True)
        create_new_profile(first_name="C", username="c@student.tue.nl", newsletter=True)
        url = "/admin/users/profile/"

        exp_status_code = 302
        exp_change_count = 1

        # act
        response = self.client.post(
            url,
            data={"action": "sync_newsletter_subscriptions", "_selected_action": [get_profile("a@student.tue.nl").pk]},
        )

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assert_changes_informed_to_user(response, exp_change_count)
        self.assert_newsletter_subscription("a@student.tue.nl", True)
        self.assert_newsletter_subscription("b@student.tue.nl", False)
        self.assert_newsletter_subscription("c@student.tue.nl", False)

    def test_sync_newsletter_subscriptions_multiple_new_subscribers(self):
        # setup
        create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=True)
        create_new_profile(first_name="B", username="b@student.tue.nl", newsletter=True)
        url = "/admin/users/profile/"

        exp_status_code = 302
        exp_change_count = 2

        # act
        response = self.client.post(
            url,
            data={
                "action": "sync_newsletter_subscriptions",
                "_selected_action": [
                    get_profile("a@student.tue.nl").pk,
                    get_profile("b@student.tue.nl").pk,
                ],
            },
        )

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assert_changes_informed_to_user(response, exp_change_count)
        self.assert_newsletter_subscription("a@student.tue.nl", True)
        self.assert_newsletter_subscription("b@student.tue.nl", True)

    def test_sync_newsletter_subscriptions_one_unsubscribes(self):
        # setup
        create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=False)
        create_new_profile(first_name="B", username="b@student.tue.nl", newsletter=True)
        create_new_profile(first_name="C", username="c@student.tue.nl", newsletter=True)
        self.newsletter_service.add_subscription(
            [
                {"email": "a@student.tue.nl", "first_name": "A", "last_name": "Broodjes"},
                {"email": "b@student.tue.nl", "first_name": "A", "last_name": "Broodjes"},
                {"email": "c@student.tue.nl", "first_name": "A", "last_name": "Broodjes"},
            ]
        )
        url = "/admin/users/profile/"

        exp_status_code = 302
        exp_change_count = 1

        # act
        response = self.client.post(
            url,
            data={"action": "sync_newsletter_subscriptions", "_selected_action": [get_profile("a@student.tue.nl").pk]},
        )

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assert_changes_informed_to_user(response, exp_change_count)
        self.assert_newsletter_subscription("a@student.tue.nl", False)
        self.assert_newsletter_subscription("b@student.tue.nl", True)
        self.assert_newsletter_subscription("c@student.tue.nl", True)

    def test_sync_newsletter_subscriptions_unauthorizederror(self):
        # setup
        create_new_profile(username="a@student.tue.nl", newsletter=True)
        url = "/admin/users/profile/"
        exp_error_msg = "Authorization error. Please check newsletter config."

        # act
        with patch.object(NewsletterService, "sync_newsletter_preferences") as mock_method:
            mock_method.side_effect = UnauthorizedError(401, "mock", "", "")
            response = self.client.post(
                url,
                data={
                    "action": "sync_newsletter_subscriptions",
                    "_selected_action": [get_profile("a@student.tue.nl").pk],
                },
            )

        # test
        self.assert_error_informed_to_user(response, 1, exp_error_msg)

    def test_sync_newsletter_subscriptions_httpexception(self):
        # setup
        create_new_profile(username="a@student.tue.nl", newsletter=True)
        url = "/admin/users/profile/"
        exp_error_msg = "Unknown HTTP error. Please check newsletter config."

        # act
        with patch.object(NewsletterService, "sync_newsletter_preferences") as mock_method:
            mock_method.side_effect = HTTPException(400, "mock", "", "")
            response = self.client.post(
                url,
                data={
                    "action": "sync_newsletter_subscriptions",
                    "_selected_action": [get_profile("a@student.tue.nl").pk],
                },
            )

        # test
        self.assert_error_informed_to_user(response, 1, exp_error_msg)

    def test_success_send_stats(self):
        # setup
        url = "/admin/users/profile/getstats/"
        exp_status_code = 200
        exp_content_type = "image/jpeg"

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_content_type, response.headers["Content-Type"])


def create_new_profile(
    first_name="Tosti",
    last_name="Broodjes",
    username="tosti@student.tue.nl",
    email="tosti@gmail.com",
    password="ikbeneenbrood",
    nationality="Dutch",
    terms_confirmed=True,
    newsletter=False,
    newsletter_recipient="TUE",
) -> Profile:
    user = User.objects.create_user(
        username=username, email=email, password=password, first_name=first_name, last_name=last_name
    )
    return Profile.objects.create(
        user=user,
        nationality=nationality,
        terms_confirmed=terms_confirmed,
        subscribed_newsletter=newsletter,
        newsletter_recipient=newsletter_recipient,
    )


def get_profile(username="tosti@student.tue.nl") -> Profile:
    return Profile.objects.get(user=User.objects.get(username=username))
