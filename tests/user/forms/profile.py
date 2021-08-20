from django.contrib.auth.models import User
from django.test import TestCase

from apps.async_requests.factory import Factory
from apps.users.forms import ProfileUpdateForm, PreferencesUpdateForm, KeyAccessUpdateForm, errors, PasswordUpdateForm
from apps.users.models import Profile
from tests.helpers import (
    get_profile_form_data,
    get_key_access_form_data,
    get_preferences_form_data,
    assert_newsletter_subscription,
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


class ProfileUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.user = generate_tue_user()
        self.newsletter_service = Factory.get_newsletter_service(True)
        self.assert_newsletter_subscription = lambda x, y: assert_newsletter_subscription(self, x, y)

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
        self.assertEqual(form.cleaned_data["department"], "Mathematics and Computer Science")

    def test_success_remove_alternative_email(self):
        # setup
        data = get_profile_form_data(email="")

        # act
        form = ProfileUpdateForm(instance=self.user, data=data)

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form["email"].initial, "tosti@gmail.com")
        self.assertEqual(form.cleaned_data["email"], "")

    def test_success_change_secondary_unsubscribed_email(self):
        # setup
        institution_email = "tosti@student.tue.nl"
        old_alt_email = "tosti@gmail.com"
        new_alt_email = "tosti@hotmail.com"

        # act
        form = ProfileUpdateForm(instance=self.user, data=get_profile_form_data(email="tosti@hotmail.com"))
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
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
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
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


class PreferencesUpdateFormTest(TestCase):
    def setUp(self) -> None:
        self.profile = generate_tue_user().profile
        self.executor = Factory.get_executor()
        self.newsletter_service = Factory.get_newsletter_service(True)

    def assert_newsletter_subscription(self, email: str, state: bool):
        # setup - none

        # act
        self.executor.execute()

        # test
        self.assertEqual(state, self.newsletter_service.is_subscribed(email))

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
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form.initial["subscribed_newsletter"], False)
        self.assertEqual(form.cleaned_data["subscribed_newsletter"], False)
        self.assert_newsletter_subscription(recipient, False)

    def test_success_newsletter_enable_institution_email(self):
        # setup
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile, data=get_preferences_form_data(subscribed_newsletter="True")
        )
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["subscribed_newsletter"], True)
        self.assert_newsletter_subscription(recipient, True)

    def test_success_newsletter_disable_institution_email(self):
        # setup
        self.profile.subscribed_newsletter = True
        self.profile.save()
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data(False))
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        self.assertEqual(form.cleaned_data["subscribed_newsletter"], False)
        self.assert_newsletter_subscription(recipient, False)

    def test_success_newsletter_enable_secondary_email(self):
        # setup
        recipient = "tosti@gmail.com"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(subscribed_newsletter=True, newsletter_recipient="ALT"),
        )
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, False)
        self.assertEqual(form.cleaned_data["subscribed_newsletter"], True)
        self.assertEqual(form["newsletter_recipient"].initial, "TUE")
        self.assertEqual(form.cleaned_data["newsletter_recipient"], "ALT")
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
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040

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
        form.is_valid()  # modifies form.instance before running save. see DjangoProject ticket #33040
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        self.assertEqual(form.cleaned_data["subscribed_newsletter"], False)
        self.assert_newsletter_subscription(recipient, False)


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
        self.assertEqual(form.cleaned_data["tue_id"], tue_id)

    def test_success_card_number_update(self):
        # setup
        card_number = "9999999"

        # act
        form = KeyAccessUpdateForm(instance=self.user, data=get_key_access_form_data(card_number=card_number))

        # test
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["card_number"], card_number)
