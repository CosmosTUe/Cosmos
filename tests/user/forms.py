from django.contrib.auth.models import User
from django.test import TestCase

from cosmos.forms import MemberCreateForm, MemberUpdateForm, ProfileCreateForm, ProfileUpdateForm


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
            },
        )
        self.assertTrue(profile_form.is_valid())
        # Save for further tests
        profile_form.save()

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
            data={"nationality": "German", "department": "Sustainable Innovation", "program": "Other"},
        )
        self.assertTrue(profile_form.is_valid())
        # Save for further tests
        profile_form.save()

    def tearDown(self) -> None:
        User.objects.get(username="tosti@student.tue.nl").delete()
        super().tearDown()


# TODO create test with invalid input: eg too long, weird characters
