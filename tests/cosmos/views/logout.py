from django.contrib.auth.models import User
from django.test import TestCase


class LogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="member@student.tue.nl", password="membersecret")
        self.client.force_login(self.user)

    def test_navbar_logs_out_with_a_form(self):
        # Django only logs out on POST; a plain link to the logout page gives an error
        response = self.client.get("/")
        self.assertContains(response, '<form method="post" action="/accounts/logout/"')
        self.assertNotContains(response, 'href="/accounts/logout/"')

    def test_logout_logs_out_and_goes_home(self):
        response = self.client.post("/accounts/logout/")
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)
