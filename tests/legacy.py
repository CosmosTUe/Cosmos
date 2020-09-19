import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.legacy.models import AuthUser, MysiteProfile
from apps.legacy.tokens import account_import_token


class LegacyTestCase(TestCase):
    databases = {"default", "legacy"}

    def test_email_link(self):
        """
        Test whether the generated link is valid and is of the correct user
        """
        auth = AuthUser.objects.create(
            username="test@example.com",
            password="12345",
            is_superuser=0,
            is_staff=0,
            is_active=0,
            date_joined=timezone.now(),
        )
        MysiteProfile.objects.create(user=auth)
        uidb64 = urlsafe_base64_encode(force_bytes(auth.username))
        token = account_import_token.make_token(auth)

        response = self.client.get(reverse("cosmos_legacy:import_user", args=(uidb64, token)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            re.findall(r" value=\"(.*?)\"", str(response.context["user_form"]["username"]))[0], auth.username
        )

    def test_already_migrated_user(self):
        """
        Test whether when a user with that username already exists, migration fails
        """
        User.objects.create_user(username="test@example.org")
        auth = AuthUser.objects.create(
            username="test@example.org",
            password="12345",
            is_superuser=0,
            is_staff=0,
            is_active=0,
            date_joined=timezone.now(),
        )
        MysiteProfile.objects.create(user=auth)
        uidb64 = urlsafe_base64_encode(force_bytes(auth.username))
        token = account_import_token.make_token(auth)

        response = self.client.get(reverse("cosmos_legacy:import_user", args=(uidb64, token)))
        self.assertContains(response, "Account import link is invalid!")

    def test_import_legacy_user(self):
        """
        Tests whether the filled in data for migration is correct
        """
        auth = AuthUser.objects.create(
            username="test@example.com",
            first_name="Mike",
            last_name="Wazowski",
            password="12345",
            is_superuser=0,
            is_staff=0,
            is_active=0,
            date_joined=timezone.now(),
        )
        profile = MysiteProfile.objects.create(
            user=auth, nationality="Dutch", department="Electrical Engineering", program="Bachelor"
        )

        uidb64 = urlsafe_base64_encode(force_bytes(auth.username))
        token = account_import_token.make_token(auth)

        response = self.client.get(reverse("cosmos_legacy:import_user", args=(uidb64, token)))
        self.assertEqual(
            re.findall(r" value=\"(.*?)\"", str(response.context["user_form"]["username"]))[0], auth.username
        )
        self.assertEqual(
            re.findall(r" value=\"(.*?)\"", str(response.context["user_form"]["first_name"]))[0], auth.first_name
        )
        self.assertEqual(
            re.findall(r" value=\"(.*?)\"", str(response.context["user_form"]["last_name"]))[0], auth.last_name
        )
        self.assertEqual(
            re.findall(r" value=\"(.*?)\" selected", str(response.context["profile_form"]["nationality"]))[0],
            profile.nationality,
        )
        self.assertEqual(
            re.findall(r" value=\"(.*?)\" selected", str(response.context["profile_form"]["department"]))[0],
            profile.department,
        )
        self.assertEqual(
            re.findall(r" value=\"(.*?)\" selected", str(response.context["profile_form"]["program"]))[0],
            profile.program,
        )
