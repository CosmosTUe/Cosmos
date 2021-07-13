from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.models.user import InstitutionTue, Profile

# Test creation & saving of User
# Test creation & saving of Profile
# Test creation & saving of Institutions
# Test correct linking @properties on Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(first_name="Mike", last_name="Wazowski", username="mike@student.tue.nl")
        self.test_profile = Profile.objects.create(user=self.test_user)
        #test_institution = InstitutionTue.objects.create(profile=test_profile)
        self.test_institution = InstitutionTue.objects.filter(profile=self.test_profile)[0]

    def test_profile_username(self):
        self.assertEqual(self.test_user.username, self.test_profile.username)

    def test_profile_institution_name(self):
        self.assertEqual(self.test_profile.institution_name, "tue")

    def test_profile_institution(self):
        self.assertEqual(self.test_profile.institution, self.test_institution)

    def test_delete_user(self):
        self.test_user.delete()
    #    self.assertTrue(not User.objects.filter(first_name="Mike"))
    #    self.assertTrue(not Profile.objects.filter(user=self.test_user))


class UserTestCase(TestCase):
    def test_profile_creation(self):
        user = User.objects.create_user(username="potato")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instance
        user.save()
        self.assertIsInstance(user.profile, Profile)
