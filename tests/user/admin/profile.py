from django.contrib.auth.models import User
from django.test import TestCase

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
