from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.forms import KeyAccessUpdateForm, PasswordUpdateForm, PreferencesUpdateForm, ProfileUpdateForm, errors
from apps.users.models import Profile
from apps.users.models.user import InstitutionTue
from tests.helpers import (
    NewsletterTestCaseMixin,
    get_key_access_form_data,
    get_preferences_form_data,
    get_profile_form_data,
)


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


class ProfileUpdateFormTest(NewsletterTestCaseMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
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
        form.full_clean()
        form.save()

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["department"].initial, "Electrical Engineering")
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.profile.institution.department, "Mathematics and Computer Science")

    def test_success_change_program(self):
        # setup
        data = get_profile_form_data(program="Master")

        # act
        form = ProfileUpdateForm(instance=self.user, data=data)
        form.full_clean()
        form.save()

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["program"].initial, "Bachelor")
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.profile.institution.program, "Master")

    def test_success_change_nationality(self):
        # setup
        data = get_profile_form_data(nationality="Belgian")

        # act
        form = ProfileUpdateForm(instance=self.user, data=data)
        form.full_clean()
        form.save()

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["nationality"].initial, "Dutch")
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.profile.nationality, "Belgian")

    def test_success_remove_alternative_email(self):
        # setup
        data = get_profile_form_data(email="")

        # act
        form = ProfileUpdateForm(instance=self.user, data=data)
        form.full_clean()
        form.save()

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["email"].initial, "tosti@gmail.com")
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.email, "")

    def test_success_change_secondary_unsubscribed_email(self):
        # setup
        institution_email = "tosti@student.tue.nl"
        old_alt_email = "tosti@gmail.com"
        new_alt_email = "tosti@hotmail.com"

        # act
        form = ProfileUpdateForm(instance=self.user, data=get_profile_form_data(email="tosti@hotmail.com"))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assert_newsletter_subscription(institution_email, False)
        self.assert_newsletter_subscription(old_alt_email, False)
        self.assert_newsletter_subscription(new_alt_email, False)

    def test_success_change_secondary_subscribed_email(self):
        # setup
        institution_email = "tosti@student.tue.nl"
        old_alt_email = "tosti@gmail.com"
        new_alt_email = "tosti@hotmail.com"
        self.user.profile.subscribed_newsletter = True
        self.user.profile.newsletter_recipient = "ALT"
        self.newsletter_service.add_subscription(
            [{"email": old_alt_email, "first_name": "Tosti", "last_name": "Broodjes"}]
        )
        self.user.profile.save()

        # act
        form = ProfileUpdateForm(instance=self.user, data=get_profile_form_data(email="tosti@hotmail.com"))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assert_newsletter_subscription(institution_email, False)
        self.assert_newsletter_subscription(old_alt_email, False)
        self.assert_newsletter_subscription(new_alt_email, True)


class PasswordUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = generate_tue_user()

    def test_empty_form(self):
        form = PasswordUpdateForm(user=self.user)
        self.assertFalse(form.has_error("__all__"))


class PreferencesUpdateFormTest(NewsletterTestCaseMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.profile = generate_tue_user().profile

    def test_prefill_data_from_db(self):
        # setup

        # act
        form = PreferencesUpdateForm(instance=self.profile)

        # test
        self.assertEqual(form.initial["subscribed_newsletter"], False)
        self.assertEqual(form.initial["newsletter_recipient"], "TUE")

    def test_success_newsletter_unchanged(self):
        # setup
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data())
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form.initial["subscribed_newsletter"], False)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assert_newsletter_subscription(recipient, False)

    def test_success_newsletter_enable_institution_email(self):
        # setup
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile, data=get_preferences_form_data(subscribed_newsletter="True")
        )
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertTrue(form.is_valid())
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, True)
        self.assert_newsletter_subscription(recipient, True)

    def test_success_newsletter_disable_institution_email(self):
        # setup
        self.profile.subscribed_newsletter = True
        self.profile.save()
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data(False))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assert_newsletter_subscription(recipient, False)

    def test_success_newsletter_enable_secondary_email(self):
        # setup
        recipient = "tosti@gmail.com"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(subscribed_newsletter=True, newsletter_recipient="ALT"),
        )
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, False)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, True)
        self.assertEqual(form["newsletter_recipient"].initial, "TUE")
        self.assertEqual(profile.newsletter_recipient, "ALT")
        self.assert_newsletter_subscription(recipient, True)

    def test_fail_newsletter_enable_secondary_email_empty(self):
        # setup
        self.profile.user.email = ""
        self.profile.user.save()

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(subscribed_newsletter=True, newsletter_recipient="ALT"),
        )
        form.full_clean()

        # test
        self.assertTrue(form.has_error("__all__", errors.INVALID_SUBSCRIBE_TO_EMPTY_EMAIL))

    def test_success_newsletter_disable_secondary_email(self):
        # setup
        self.profile.subscribed_newsletter = True
        self.profile.newsletter_recipient = "ALT"
        self.profile.save()

        recipient = "tosti@gmail.com"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data(subscribed_newsletter=False))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assert_newsletter_subscription(recipient, False)


class KeyAccessUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.institution = generate_tue_user().profile.institution

    def test_prefill_data_from_db(self):
        # setup

        # act
        form = KeyAccessUpdateForm(instance=self.institution)

        # test
        self.assertEqual(form["tue_id"].initial, "")
        self.assertEqual(form["card_number"].initial, "")

    def test_fail_login_id_submitted_as_tue_id(self):
        # setup
        tue_id = "20201234"

        # act
        form = KeyAccessUpdateForm(instance=self.institution, data=get_key_access_form_data(tue_id=tue_id))

        # test
        self.assertTrue(form.has_error("tue_id", errors.INVALID_TUE_ID))

    def test_success_tue_id_update(self):
        # setup
        tue_id = "0000000"

        # act
        form = KeyAccessUpdateForm(instance=self.institution, data=get_key_access_form_data(tue_id=tue_id))
        form.full_clean()
        form.save()

        # test
        self.assertTrue(form.is_valid())
        institution = InstitutionTue.objects.get(pk=self.institution.pk)
        self.assertEqual(institution.tue_id, tue_id)

    def test_success_card_number_update(self):
        # setup
        card_number = "9999999"

        # act
        form = KeyAccessUpdateForm(instance=self.institution, data=get_key_access_form_data(card_number=card_number))
        form.full_clean()
        form.save()

        # test
        self.assertTrue(form.is_valid())
        institution = InstitutionTue.objects.get(pk=self.institution.pk)
        self.assertEqual(institution.card_number, card_number)
