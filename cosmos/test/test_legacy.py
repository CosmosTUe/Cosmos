from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from legacy.models import AuthUser, MysiteProfile
from legacy.tokens import account_import_token


class LegacyTestCase(TestCase):
    databases = {"default", "legacy"}

    def test_legacy_profile_import(self):
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

        response = self.client.get(reverse("import_user", args=(uidb64, token)))
        self.assertEqual(response.status_code, 200)
