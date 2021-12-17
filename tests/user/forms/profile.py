from django.contrib.auth.models import User
from django.test import TestCase

from apps.async_requests.constants import NEWSLETTER_LIST_ID
from apps.users.forms import PasswordUpdateForm, PreferencesUpdateForm, ProfileUpdateForm, error_codes
from apps.users.models import Profile
from tests.helpers import NewsletterTestCaseMixin, get_preferences_form_data, get_profile_form_data


def generate_tue_user(
    username="tosti@student.tue.nl",
    email="tosti@gmail.com",
    password="ikbeneenbrood",
    nationality="Dutch",
    subscribed_newsletter=False,
    department="Electrical Engineering",
    program="Bachelor",
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
            [{"email": old_alt_email, "first_name": "Tosti", "last_name": "Broodjes"}], NEWSLETTER_LIST_ID
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
        self.assertEqual(form.initial["subscribed_gmm_invite"], False)
        self.assertEqual(form.initial["newsletter_recipient"], "TUE")

    def test_success_newsletter_unchanged(self):
        # setup
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data())
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form.instance.subscribed_newsletter, False)
        self.assertEqual(form.instance.subscribed_gmm_invite, False)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assertEqual(profile.subscribed_gmm_invite, False)
        self.assert_newsletter_subscription(recipient, False)
        self.assert_gmm_invite_subscription(recipient, False)

    def test_success_newsletter_enable_newsletter_sub_on_institution_email(self):
        # setup
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data(subscribed_newsletter=True))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertTrue(form.is_valid())
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, True)
        self.assertEqual(profile.subscribed_gmm_invite, False)
        self.assert_newsletter_subscription(recipient, True)
        self.assert_gmm_invite_subscription(recipient, False)

    def test_success_newsletter_disable_newsletter_sub_on_institution_email(self):
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
        self.assertEqual(profile.subscribed_gmm_invite, False)
        self.assert_newsletter_subscription(recipient, False)
        self.assert_gmm_invite_subscription(recipient, False)

    def test_success_newsletter_enable_gmm_invite_sub_on_institution_email(self):
        # setup
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data(subscribed_gmm_invite=True))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertTrue(form.is_valid())
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assertEqual(profile.subscribed_gmm_invite, True)
        self.assert_newsletter_subscription(recipient, False)
        self.assert_gmm_invite_subscription(recipient, True)

    def test_success_newsletter_disable_gmm_invite_sub_on_institution_email(self):
        # setup
        self.profile.subscribed_newsletter = True
        self.profile.save()
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(instance=self.profile, data=get_preferences_form_data(subscribed_gmm_invite=True))
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assert_newsletter_subscription(recipient, False)
        self.assert_gmm_invite_subscription(recipient, True)

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
        self.assertEqual(profile.subscribed_gmm_invite, False)
        self.assertEqual(form["newsletter_recipient"].initial, "TUE")
        self.assertEqual(profile.newsletter_recipient, "ALT")
        self.assert_newsletter_subscription(recipient, True)
        self.assert_gmm_invite_subscription(recipient, False)

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
        self.assertTrue(form.has_error("__all__", error_codes.INVALID_SUBSCRIBE_TO_EMPTY_EMAIL))

    def test_fail_gmm_invite_enable_secondary_email_empty(self):
        # setup
        self.profile.user.email = ""
        self.profile.user.save()

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(subscribed_gmm_invite=True, newsletter_recipient="ALT"),
        )
        form.full_clean()

        # test
        self.assertTrue(form.has_error("__all__", error_codes.INVALID_SUBSCRIBE_TO_EMPTY_EMAIL))

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
        self.assertEqual(profile.subscribed_gmm_invite, False)
        self.assert_newsletter_subscription(recipient, False)
        self.assert_gmm_invite_subscription(recipient, False)

    def test_subscribe_all_primary_email(self):
        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(
                subscribed_newsletter=True, subscribed_gmm_invite=True, newsletter_recipient="TUE"
            ),
        )
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, False)
        self.assertEqual(form["subscribed_gmm_invite"].initial, False)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, True)
        self.assertEqual(profile.subscribed_gmm_invite, True)
        self.assert_newsletter_subscription(recipient, True)
        self.assert_gmm_invite_subscription(recipient, True)

    def test_unsubscribe_all_primary_email(self):
        # setup
        self.profile.subscribed_newsletter = True
        self.profile.subscribed_gmm_invite = True
        self.profile.newsletter_recipient = "TUE"
        self.profile.save()

        recipient = "tosti@student.tue.nl"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(
                subscribed_newsletter=False, subscribed_gmm_invite=False, newsletter_recipient="TUE"
            ),
        )
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        self.assertEqual(form["subscribed_gmm_invite"].initial, True)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, False)
        self.assertEqual(profile.subscribed_gmm_invite, False)
        self.assert_newsletter_subscription(recipient, False)
        self.assert_gmm_invite_subscription(recipient, False)

    def test_subscribe_all_primary_to_secondary_email(self):
        # setup
        self.profile.subscribed_newsletter = True
        self.profile.subscribed_gmm_invite = True
        self.profile.newsletter_recipient = "TUE"
        self.profile.save()

        recipient = "tosti@gmail.com"

        # act
        form = PreferencesUpdateForm(
            instance=self.profile,
            data=get_preferences_form_data(
                subscribed_newsletter=True, subscribed_gmm_invite=True, newsletter_recipient="ALT"
            ),
        )
        form.full_clean()
        form.save()  # runs update_newsletter_preferences

        # test
        self.assertEqual(form["subscribed_newsletter"].initial, True)
        self.assertEqual(form["subscribed_gmm_invite"].initial, True)
        profile = Profile.objects.get(pk=self.profile.pk)
        self.assertEqual(profile.subscribed_newsletter, True)
        self.assertEqual(profile.subscribed_gmm_invite, True)
        self.assert_newsletter_subscription(recipient, True)
        self.assert_gmm_invite_subscription(recipient, True)
