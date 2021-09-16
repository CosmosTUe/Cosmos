from django.contrib.auth.models import User
from django.test import TestCase


class DoorSensorTest(TestCase):
    def create_url(self, token, status):
        return "/door-status?access_token=" + str(token) + "&status=" + str(status)

    def test_wrong_token(self):
        response = self.client.get(self.create_url(70000, 1))
        self.assertEqual(401, response.status_code)

    def test_correct_token(self):
        response = self.client.get(self.create_url(696969, 1))
        self.assertContains(response, "Updated door status", status_code=200)

    def test_status_forbidden_for_public(self):
        self.client.logout()
        response = self.client.get("/")
        self.assertNotContains(response, 'id="cr-door"')

    def test_status_open(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")
        self.client.get(self.create_url(696969, 1))
        response = self.client.get("/")

        self.assertContains(response, 'id="cr-door" class="bi bi-unlock-fill')

    def test_status_closed(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")
        self.client.get(self.create_url(696969, 0))
        response = self.client.get("/")

        self.assertContains(response, 'id="cr-door" class="bi bi-lock-fill')
