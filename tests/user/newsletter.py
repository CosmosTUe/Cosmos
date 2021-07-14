from django.contrib.auth.models import User
from django.test import TestCase

from apps.async_requests.factory import Factory
from apps.users.models import Profile


class NewsletterLogic(TestCase):
    def setUp(self) -> None:
        self.service = Factory.get_newsletter_service()
        self.executor = Factory.get_executor()
        self.inst_email = "tosti@student.tue.nl"
        self.alt_email = "tosti@gmail.com"
        self.user = User.objects.create_user(
            username=self.inst_email,
            email=self.alt_email,
        )
        self.user.profile = Profile(
            user=self.user, nationality="Dutch", terms_confirmed=True, subscribed_newsletter=False
        )

    def tearDown(self) -> None:
        User.objects.get(username=self.inst_email).delete()
        super().tearDown()

    def test_is_subscribed_false(self):
        # setup - none

        # act
        result = self.service.is_subscribed(self.user.username)

        # test
        self.assertFalse(result, msg="is_subscribed false")

    def test_is_subscribed_true(self):
        # setup
        self.service.add_subscription(
            [{"email": self.alt_email, "first_name": self.user.first_name, "last_name": self.user.last_name}]
        )

        # act
        result = self.service.is_subscribed(self.alt_email)

        # test
        self.assertTrue(result)

    def test_add(self):
        # setup - none

        # act
        success = self.service.add_subscription(
            [{"email": self.alt_email, "first_name": self.user.first_name, "last_name": self.user.last_name}]
        )

        # test
        result = self.service.is_subscribed(self.alt_email)
        self.assertTrue(success)
        self.assertTrue(result)

    def test_remove_empty_db(self):
        # setup - none

        # act
        success = self.service.remove_subscription([self.alt_email])

        # test
        result = self.service.is_subscribed(self.alt_email)
        self.assertTrue(success)
        self.assertFalse(result)

    def test_remove_filled_db(self):
        # setup
        self.service.add_subscription(
            [{"email": self.alt_email, "first_name": self.user.first_name, "last_name": self.user.last_name}]
        )

        # act
        success = self.service.remove_subscription([self.alt_email])

        # test
        result = self.service.is_subscribed(self.alt_email)
        self.assertTrue(success)
        self.assertFalse(result)

    def assert_subscription_states(self, exp_tue, exp_alt):
        result_tue = self.service.is_subscribed(self.inst_email)
        result_alt = self.service.is_subscribed(self.alt_email)
        self.assertEqual(exp_tue, result_tue)
        self.assertEqual(exp_alt, result_alt)

    def _test_update(self, exp_tue, exp_alt, old_sub=False, old_rec="TUE", new_sub=False, new_rec="TUE"):
        """
        Helper function to speed up testing

        :param exp_tue: expected subscription for TUe email
        :param exp_alt: expected subscription for alternative email
        :param old_sub: old subscription state
        :param old_rec: old subscription recipient
        :param new_sub: old subscription state
        :param new_rec: old subscription recipient
        :return:
        """
        # setup
        self.user.profile.subscribed_newsletter = new_sub
        self.user.profile.newsletter_recipient = new_rec

        # act
        self.service.update_newsletter_preferences(self.user.profile, old_sub, old_rec)
        Factory.get_executor().execute()

        # test
        self.assert_subscription_states(exp_tue, exp_alt)

    def test_update_unsubscribed_user_unchanged(self):
        self._test_update(False, False)

    def test_update_unsubscribed_user_subscribes(self):
        self._test_update(True, False, new_sub=True)

    def test_update_subscribed_user_unchanged(self):
        # setup
        self.service.add_subscription(
            [{"email": self.inst_email, "first_name": self.user.first_name, "last_name": self.user.last_name}]
        )
        self.executor.execute()

        # act
        self._test_update(True, False, old_sub=True, new_sub=True)

    def test_update_user_change_from_inst_email_to_alt_email(self):
        # setup
        self.service.add_subscription(
            [{"email": self.inst_email, "first_name": self.user.first_name, "last_name": self.user.last_name}]
        )
        self.executor.execute()

        # act
        self._test_update(False, True, old_sub=True, new_sub=True, new_rec="ALT")

    def test_update_user_change_from_alt_email_to_inst_email(self):
        # setup
        self.service.add_subscription(
            [{"email": self.alt_email, "first_name": self.user.first_name, "last_name": self.user.last_name}]
        )
        self.executor.execute()

        # act
        self._test_update(True, False, old_sub=True, old_rec="ALT", new_sub=True)
