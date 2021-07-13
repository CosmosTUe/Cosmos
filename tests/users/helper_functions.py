from django.test import TestCase

from apps.users.helper_functions import is_fontys_email, is_tue_email


class HelperFunctionsTestCase(TestCase):
    def test_fail_is_tue_email(self):
        self.assertFalse(is_tue_email("mike@tue.nl"))
        self.assertFalse(is_tue_email("mike@gmail.com"))
        self.assertFalse(is_tue_email("mike@outlook.org"))

    def test_success_is_tue_email(self):
        self.assertTrue(is_tue_email("mike@student.tue.nl"))
        self.assertTrue(is_tue_email("mike@alumni.tue.nl"))
        self.assertTrue(is_tue_email("alice2@student.tue.nl"))

    def test_fail_is_fontys_email(self):
        self.assertFalse(is_tue_email("mike@gmail.com"))
        self.assertFalse(is_tue_email("mike@outlook.org"))

    def test_success_is_fontys_email(self):
        self.assertTrue(is_fontys_email("mike@fontys.nl"))
