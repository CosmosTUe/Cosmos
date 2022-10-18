from http.client import HTTPException
from unittest.mock import patch

from django.contrib import messages
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase
from newsletter.models import Newsletter
from python_http_client import UnauthorizedError

from apps.async_requests.newsletter.newsletter_service import NewsletterService
from apps.users.admin import ProfileAdmin
from apps.users.models import Profile
from mocks.request import MockRequest
from tests.helpers import BaseAdminTestCaseMixin, NewsletterTestCaseMixin

mock_msgs = []


def mock_message_user(_, message, level=messages.INFO, *args, **kwargs):
    mock_msgs.append((message, level))


class ProfileAdminTest(NewsletterTestCaseMixin, TestCase):
    def setUp(self):
        super(ProfileAdminTest, self).setUp()
        self.request = MockRequest(superuser=True)
        self.site = AdminSite()
        self.admin = ProfileAdmin(Profile, self.site)
        self.admin.message_user = mock_message_user  # MagicMock(return_value=None)

    def tearDown(self) -> None:
        mock_msgs.clear()

    def assert_changes_informed_to_user(self, change_count):
        exp_message_count = 2
        exp_loading_msg = f"Sending {change_count} messages..."
        exp_ending_msg = f"{change_count} newsletter preferences updated!"

        self.assertEqual(exp_message_count, len(mock_msgs))
        self.assertEqual(exp_loading_msg, str(mock_msgs[0][0]))
        self.assertEqual(messages.INFO, mock_msgs[0][1])
        self.assertEqual(exp_ending_msg, str(mock_msgs[1][0]))
        self.assertEqual(messages.SUCCESS, mock_msgs[1][1])

    def assert_error_informed_to_user(self, change_count, error_msg):
        exp_message_count = 2
        exp_loading_msg = f"Sending {change_count} messages..."

        self.assertEqual(exp_message_count, len(mock_msgs))
        self.assertEqual(exp_loading_msg, str(mock_msgs[0][0]))
        self.assertEqual(error_msg, str(mock_msgs[1][0]))
        self.assertEqual(messages.ERROR, mock_msgs[1][1])

    def create_new_profile(
        self,
        first_name="Tosti",
        last_name="Broodjes",
        username="tosti@student.tue.nl",
        email="tosti@gmail.com",
        password="ikbeneenbrood",
        nationality="Dutch",
        terms_confirmed=True,
        newsletter=False,
        gmm_invite=False,
        newsletter_recipient="TUE",
    ) -> Profile:
        user = User(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        return Profile(
            user=user,
            nationality=nationality,
            terms_confirmed=terms_confirmed,
            subscribed_newsletter=newsletter,
            subscribed_gmm_invite=gmm_invite,
            newsletter_recipient=newsletter_recipient,
        )

    def test_newsletters_not_created(self):
        # setup
        Newsletter.objects.all().delete()
        a = self.create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=True)
        query = [a]
        # act
        self.admin.sync_newsletter_subscriptions(self.request, query)
        # test
        self.assert_error_informed_to_user(
            1, "Missing Newsletter object(s). Ensure Newsletter objects have the following slugs: cosmos-news, gmm."
        )

    def test_sync_newsletter_subscriptions_single(self):
        # setup
        a = self.create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=True)
        query = [a]
        # act
        self.admin.sync_newsletter_subscriptions(self.request, query)
        # test
        self.assert_changes_informed_to_user(1)
        self.assert_newsletter_subscription("a@student.tue.nl", True)
        self.assert_gmm_invite_subscription("a@student.tue.nl", False)

    def test_sync_newsletter_subscriptions_multiple_subscribers(self):
        # setup
        a = self.create_new_profile(first_name="A", username="a@student.tue.nl", newsletter=True)
        b = self.create_new_profile(first_name="B", username="b@student.tue.nl", newsletter=True)
        query = [a, b]
        # act
        self.admin.sync_newsletter_subscriptions(self.request, query)
        # test
        self.assert_changes_informed_to_user(2)
        self.assert_newsletter_subscription("a@student.tue.nl", True)
        self.assert_gmm_invite_subscription("a@student.tue.nl", False)
        self.assert_newsletter_subscription("b@student.tue.nl", True)
        self.assert_gmm_invite_subscription("b@student.tue.nl", False)

    def test_sync_newsletter_subscriptions_unsubscribe(self):
        # setup
        a = self.create_new_profile(first_name="A", username="a@student.tue.nl")
        query = [a]
        # act
        self.admin.sync_newsletter_subscriptions(self.request, query)
        # test
        self.assert_changes_informed_to_user(1)
        self.assert_newsletter_subscription("a@student.tue.nl", False)
        self.assert_gmm_invite_subscription("a@student.tue.nl", False)

    def test_sync_newsletter_subscriptions_unauthorizederror(self):
        # setup
        a = create_new_profile(username="a@student.tue.nl", newsletter=True)
        query = [a]
        exp_error_msg = "Authorization error. Please check newsletter config."
        # act
        with patch.object(NewsletterService, "sync_subscription_preferences") as mock_method:
            mock_method.side_effect = UnauthorizedError(401, "mock", "", "")
            self.admin.sync_newsletter_subscriptions(self.request, query)
        # test
        self.assert_error_informed_to_user(1, exp_error_msg)

    def test_sync_newsletter_subscriptions_httpexception(self):
        # setup
        a = create_new_profile(username="a@student.tue.nl", newsletter=True)
        query = [a]
        exp_error_msg = "Unknown HTTP error. Please check newsletter config."
        # act
        with patch.object(NewsletterService, "sync_subscription_preferences") as mock_method:
            mock_method.side_effect = HTTPException(400, "mock", "", "")
            self.admin.sync_newsletter_subscriptions(self.request, query)
        # test
        self.assert_error_informed_to_user(1, exp_error_msg)


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
