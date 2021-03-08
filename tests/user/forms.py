from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.forms import (
    MemberCreateForm,
    MemberUpdateForm,
    ProfileCreateForm,
    ProfileUpdateForm,
    newsletter_service,
)

from apps.async_requests.factory import Factory


class UserForms(TestCase):
    def setUp(self) -> None:
        """
        Test successful registration
        """
        user_form = MemberCreateForm(
            data={
                "username": "tosti@student.tue.nl",
                "email": "tosti@gmail.com",
                "first_name": "Tosti",
                "last_name": "Broodjes",
                "password1": "ikbeneenbrood",
                "password2": "ikbeneenbrood",
            }
        )
        self.assertTrue(user_form.is_valid())
        # Save for further tests
        user = user_form.save()

        profile_form = ProfileCreateForm(
            instance=user.profile,
            data={
                "nationality": "Dutch",
                "department": "Sustainable Innovation",
                "program": "Other",
                "terms_confirmed": True,
                "subscribed_newsletter": False,
                "newsletter_recipient": "TUE",
            },
        )
        self.assertTrue(profile_form.is_valid())
        # Save for further tests
        profile_form.save()
        newsletter_service.db.clear()

    def test_fail_register_duplicate(self):
        """
        Test invalid registration. Duplicate User.
        """
        user_form = MemberCreateForm(data={"username": "tosti@student.tue.nl"})
        self.assertTrue(user_form.has_error("username", "duplicate_user"))
        self.assertFalse(user_form.is_valid())

    def test_fail_register_username_gmail(self):
        """
        Test invalid registration. Gmail provided as username
        """
        user_form = MemberCreateForm(data={"username": "tosti@gmail.com"})
        self.assertTrue(user_form.has_error("username", "nontue_email"))

    def test_fail_register_username_fake_tue(self):
        """
        Test invalid registration. Fake TUe email provided as username
        """
        user_form = MemberCreateForm(data={"username": "tosti@cosmostue.nl"})
        self.assertTrue(user_form.has_error("username", "nontue_email"))

    def test_fail_register_missing_profile(self):
        """
        Test invalid registration. Missing profile.
        """
        profile_form = ProfileCreateForm(data={})
        self.assertFalse(profile_form.is_valid())

    def test_success_update(self):
        """
        Test successful update.
        """
        user = User.objects.get(username="tosti@student.tue.nl")
        user_form = MemberUpdateForm(
            instance=user,
            data={
                "username": "tosti@student.tue.nl",
                "email": "tosti@gmail.com",
                "first_name": "Tosti",
                "last_name": "Broodjes",
            },
        )
        self.assertTrue(user_form.is_valid())
        # Save for further tests
        user_form.save()

        profile_form = ProfileUpdateForm(
            instance=user.profile,
            data={
                "nationality": "German",
                "department": "Sustainable Innovation",
                "program": "Other",
                "subscribed_newsletter": True,
                "newsletter_recipient": "TUE",
            },
        )
        self.assertTrue(profile_form.is_valid())
        # Save for further tests
        profile_form.save()

        Factory.get_executor().execute()

        self.assertTrue(newsletter_service.is_subscribed("tosti@student.tue.nl"))
        self.assertFalse(newsletter_service.is_subscribed("tosti@gmail.com"))

    def test_update_newsletter(self):
        """
        Test successful update.
        """
        user = User.objects.get(username="tosti@student.tue.nl")
        profile_form = ProfileUpdateForm(
            instance=user.profile,
            data={
                "nationality": "German",
                "department": "Sustainable Innovation",
                "program": "Other",
                "subscribed_newsletter": True,
                "newsletter_recipient": "ALT",
            },
        )
        self.assertTrue(profile_form.is_valid())
        # Save for further tests
        profile_form.save()

        Factory.get_executor().execute()

        self.assertFalse(newsletter_service.is_subscribed("tosti@student.tue.nl"))
        self.assertTrue(newsletter_service.is_subscribed("tosti@gmail.com"))

    def tearDown(self) -> None:
        User.objects.get(username="tosti@student.tue.nl").delete()
        super().tearDown()
