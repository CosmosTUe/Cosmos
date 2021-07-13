from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.mail import create_confirm_account_email
from apps.users.models.user import Profile


class UsersMailTestCase(TestCase):
    def test_valid_confirmation_email(self):
        first_name = "mike"
        username = "mike@student.tue.nl"
        user = User.objects.create(
            first_name=first_name,
            last_name="wazowski",
            username=username,
            email=username,
            password="abc123",
        )
        profile = Profile.objects.create(user=user)
        email = create_confirm_account_email(profile)
        self.assertTrue(email.to[0] == username)
        self.assertTrue(first_name in email.body)
        # TODO: validate confirmation url
