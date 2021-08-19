from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.forms import ProfileUpdateForm, PreferencesUpdateForm, KeyAccessUpdateForm, errors, PasswordUpdateForm
from apps.users.models import Profile
from tests.helpers import get_profile_form_data, get_key_access_form_data


def generate_tue_user(
    username="tosti@student.tue.nl",
    email="tosti@gmail.com",
    password="ikbeneenbrood",
    nationality="Dutch",
    subscribed_newsletter=False,
    department="Electrical Engineering",
    program="Bachelor",
    tue_id=None,
    card_number=None,
):
    user = User.objects.create_user(username=username, email=email, password=password)
    profile = Profile.objects.create(
        user=user,
        nationality=nationality,
        terms_confirmed=True,
        subscribed_newsletter=subscribed_newsletter,
    )
    institution = profile.institution
    institution.department = department
    institution.program = program
    if tue_id is not None:
        institution.tue_id = tue_id
    if card_number is not None:
        institution.card_number = card_number
    institution.save()
    return user


class ProfileUpdateFormTest(TestCase):
    def generate_form(self):
        pass

    def setUp(self) -> None:
        self.user = generate_tue_user()

    def test_prefill_data_from_db(self):
        # setup

        # act
        form = ProfileUpdateForm(instance=self.user)

        # test
        self.assertEqual(form["username"].initial, "tosti@student.tue.nl")
        self.assertEqual(form["email"].initial, "tosti@gmail.com")
        self.assertEqual(form["nationality"].initial, "Dutch")
        self.assertEqual(form["department"].initial, "Electrical Engineering")
        self.assertEqual(form["program"].initial, "Bachelor")
        self.assertEqual(form["study"].initial, None)

    def test_success_change_department(self):
        # setup
        data = get_profile_form_data(department="Mathematics and Computer Science")

        # act
        form = ProfileUpdateForm(instance=self.user, data=data)

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["department"].initial, "Electrical Engineering")
        self.assertEqual(form["department"].data, "Mathematics and Computer Science")

    def test_success_remove_alternative_email(self):
        # setup
        data = get_profile_form_data(email="")

        # act
        form = ProfileUpdateForm(instance=self.user, data=data)

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["email"].initial, "tosti@gmail.com")
        self.assertEqual(form["email"].data, "")


class PasswordUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = generate_tue_user()

    def test_empty_form(self):
        form = PasswordUpdateForm(user=self.user)
        self.assertTrue(form.has_error("__all__"))


class PreferencesUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = generate_tue_user()

    def test_prefill_data_from_db(self):
        # setup

        # act
        form = PreferencesUpdateForm(instance=self.user)

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, self.user.profile.subscribed_newsletter)
        self.assertEqual(form["newsletter_recipient"].initial, self.user.profile.newsletter_recipient)


class KeyAccessUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = generate_tue_user()

    def test_prefill_data_from_db(self):
        # setup

        # act
        form = KeyAccessUpdateForm(instance=self.user)

        # test
        self.assertEqual(form["tue_id"].initial, None)
        self.assertEqual(form["card_number"].initial, None)

    def test_fail_login_id_submitted_as_tue_id(self):
        # setup
        tue_id = "20201234"

        # act
        form = KeyAccessUpdateForm(instance=self.user, data=get_key_access_form_data(tue_id=tue_id))

        # test
        self.assertTrue(form.has_error("tue_id", errors.INVALID_TUE_ID))

    def test_success_tue_id_update(self):
        # setup
        tue_id = "0000000"

        # act
        form = KeyAccessUpdateForm(instance=self.user, data=get_key_access_form_data(tue_id=tue_id))

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["tue_id"].data, tue_id)

    def test_success_card_number_update(self):
        # setup
        card_number = "9999999"

        # act
        form = KeyAccessUpdateForm(instance=self.user, data=get_key_access_form_data(card_number=card_number))

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["card_number"].data, card_number)
