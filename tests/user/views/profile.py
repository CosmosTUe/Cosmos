from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.async_requests.factory import Factory
from apps.users.models import Profile
from tests.helpers import get_key_access_form_data, get_profile_form_data


def get_logged_in_client() -> Client:
    c = Client()
    c.login(username="tosti@student.tue.nl", password="ikbeneenbrood")
    return c


def get_logged_out_client() -> Client:
    c = Client()
    c.logout()
    return c


class ProfileUpdateFlowTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="tosti@student.tue.nl", email="tosti@gmail.com", password="ikbeneenbrood"
        )
        Profile(
            user=self.user,
            nationality="Dutch",
            terms_confirmed=True,
            subscribed_newsletter=False,
        ).save()
        self.executor = Factory.get_executor()
        self.newsletter_service = Factory.get_newsletter_service(True)

    def test_success_do_nothing(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/"

        exp_status_code = 200

        # act
        response = c.get(url, data=get_profile_form_data())

        # test
        self.assertEqual(exp_status_code, response.status_code)

    def test_success_change_department(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/"
        exp_department = "Electrical Engineering"

        # act
        response = c.post(url, data=get_profile_form_data(department="Electrical Engineering"))

        # test
        form_data = response.wsgi_request.POST
        self.assertEqual(302, response.status_code)
        self.assertEqual(exp_department, form_data["department"])

    # def test_fail_change_institution_email(self):
    #     # setup
    #     c = get_logged_in_client()
    #     url = "/accounts/profile/"
    #     exp_error_msg = "Invalid operation. Please contact the website admins to change profile institution."
    #     exp_status_code = 200

    #     # act
    #     response = c.post(url, data=get_profile_form_data(username="tosti@fontys.nl"))

    #     # test
    #     self.assertEqual(exp_status_code, response.status_code)
    #     self.assertContains(response, exp_error_msg)

    def test_fail_logged_out(self):
        # setup
        c = get_logged_out_client()
        url = "/accounts/profile/"

        exp_status_code = 302
        exp_url = "/accounts/login/?next=/accounts/profile/"

        # act
        response = c.get(url)

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_url, response.url)

    def test_success_remove_alternative_email(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/"
        exp_alt_email = ""

        # act
        response = c.post(url, data=get_profile_form_data(email=""))

        # test
        form_data = response.wsgi_request.POST
        self.assertEqual(302, response.status_code)
        self.assertEqual(exp_alt_email, form_data["email"])

    def test_success_key_access_unchanged(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/#key-access"

        exp_status_code = 302

        # act
        response = c.post(url, data=get_key_access_form_data())

        # test
        self.assertEqual(exp_status_code, response.status_code)
