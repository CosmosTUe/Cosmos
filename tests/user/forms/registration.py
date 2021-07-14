from django.contrib.auth.models import User
from django.test import TestCase

from apps.async_requests.factory import Factory
from apps.users.forms import RegisterUserForm
from apps.users.forms.errors import DUPLICATE_EMAIL, INVALID_EMAIL

newsletter_service = Factory.get_newsletter_service()


class RegisterUserFormTest(TestCase):
    @staticmethod
    def generate_form(
        first_name="Tosti",
        last_name="Broodjes",
        username="tosti@student.tue.nl",
        email="tosti@gmail.com",
        pwd1="ikbeneenbrood",
        pwd2="ikbeneenbrood",
        nationality="Dutch",
        terms_confirmed=True,
        newsletter=False,
    ) -> RegisterUserForm:
        return RegisterUserForm(
            data={
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "email": email,
                "password1": pwd1,
                "password2": pwd2,
                "nationality": nationality,
                "terms_confirmed": terms_confirmed,
                "subscribed_newsletter": newsletter,
            }
        )

    def test_success_tue(self):
        """
        TUe User registration success
        """
        # setup
        exp_institution = "tue"

        # act
        form = self.generate_form()
        user = form.save()

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(user.profile.institution_name, exp_institution)

    def test_success_fontys(self):
        """
        Fontys User registration success
        """
        # setup
        exp_institution = "fontys"

        # act
        form = self.generate_form(username="tosti@fontys.nl")
        user = form.save()

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(user.profile.institution_name, exp_institution)

    def test_fail_register_duplicate(self):
        """
        User registration fails when duplicate user is found.
        """
        # setup
        self.generate_form().save()
        exp_error = DUPLICATE_EMAIL

        # act
        form = self.generate_form()

        # test
        self.assertTrue(form.has_error("username", exp_error))
        self.assertFalse(form.is_valid())

    def test_fail_register_username_gmail(self):
        """
        User registration fails when non-institution email is given as username
        """
        # setup - none
        username = "tosti@gmail.com"
        exp_error = INVALID_EMAIL

        # act
        form = self.generate_form(username=username)

        # test
        self.assertTrue(form.has_error("username", exp_error))
        self.assertFalse(form.is_valid())

    def test_fail_register_username_fake_tue(self):
        """
        User registration fails when fake TUe email is provided as username
        """
        # setup
        username = "tosti@cosmostue.com"
        exp_error = INVALID_EMAIL

        # act
        form = self.generate_form(username=username)

        # test
        self.assertTrue(form.has_error("username", exp_error))
        self.assertFalse(form.is_valid())

    def tearDown(self) -> None:
        User.objects.all().delete()
        super().tearDown()
