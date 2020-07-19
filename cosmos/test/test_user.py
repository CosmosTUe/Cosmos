from django.test import TestCase

from cosmos.models.user import Profile, User


class UserTestCase(TestCase):
    def test_profile_creation(self):
        user = User.objects.create(username="potato")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instance
        user.save()
        self.assertIsInstance(user.profile, Profile)
