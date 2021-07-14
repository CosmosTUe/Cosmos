from django.contrib.auth.models import User
from django.test import Client, TestCase

from apps.async_requests.factory import Factory
from apps.users.models import Profile


def get_logged_in_client() -> Client:
    c = Client()
    c.login(username="tosti@student.tue.nl", password="ikbeneenbrood")
    return c


def get_logged_out_client() -> Client:
    c = Client()
    c.logout()
    return c


def get_profile_form_data(
    first_name="Tosti",
    last_name="Broodjes",
    username="tosti@student.tue.nl",
    email="tosti@gmail.com",
    nationality="Dutch",
    department="Electrical Engineering",
    program="Bachelor",
    study="",
):
    output = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "nationality": nationality,
        "department": department,
        "program": program,
        "study": study,
        "save_profile": "Submit",
    }
    return {k: v for k, v in output.items() if v is not None}


def get_preferences_form_data(subscribed_newsletter=False, newsletter_recipient="TUE"):
    output = {"newsletter_recipient": newsletter_recipient, "save_preferences": "Submit"}
    if subscribed_newsletter:
        output["subscribed_newsletter"] = "on"

    return output


def get_key_access_form_data(tue_id="", card_number=""):
    return {"tue_id": tue_id, "card_number": card_number, "save_key_access": "Submit"}


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
        self.newsletter_service = Factory.get_newsletter_service()

    def test_success_do_nothing(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/"

        exp_status_code = 200
        # act
        response = c.get(url)

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
        self.assertEqual(200, response.status_code)
        self.assertTrue(exp_department, form_data["department"])

    def test_fail_change_institution_email(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/"
        exp_error_msg = "Invalid operation. Please contact the website admins to change profile institution."

        # act
        response = c.post(url, data=get_profile_form_data(username="tosti@fontys.nl"))

        # test
        self.assertEqual(200, response.status_code)
        self.assertContains(response, exp_error_msg)

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

    def assert_newsletter_subscription(self, email: str, state: bool):
        # setup - none

        # act
        self.executor.execute()

        # test
        self.assertEqual(state, self.newsletter_service.is_subscribed(email))

    def test_success_newsletter_unchanged(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/#preferences"
        recipient = "tosti@student.tue.nl"
        newsletter_field = "subscribed_newsletter"

        exp_status_code = 302

        # act
        response = c.post(url, data=get_preferences_form_data())

        # test
        form_data = response.wsgi_request.POST

        self.assertEqual(exp_status_code, response.status_code)
        self.assertNotIn(newsletter_field, form_data)
        self.assert_newsletter_subscription(recipient, False)

    def test_success_newsletter_enable(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/#preferences"
        recipient = "tosti@student.tue.nl"
        newsletter_field = "subscribed_newsletter"

        exp_status_code = 302
        exp_newsletter = "on"

        # act
        response = c.post(url, data=get_preferences_form_data(True))

        # test
        form_data = response.wsgi_request.POST

        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_newsletter, form_data[newsletter_field])
        self.assert_newsletter_subscription(recipient, True)

    def test_success_newsletter_disable(self):
        # setup
        self.user.profile.subscribed_newsletter = True
        self.user.profile.save()

        c = get_logged_in_client()
        url = "/accounts/profile/#preferences"
        recipient = "tosti@student.tue.nl"
        newsletter_field = "subscribed_newsletter"

        exp_status_code = 302

        # act
        response = c.post(url, data=get_preferences_form_data(False))

        # test
        form_data = response.wsgi_request.POST

        self.assertEqual(exp_status_code, response.status_code)
        self.assertNotIn(newsletter_field, form_data)
        self.assert_newsletter_subscription(recipient, False)

    def test_success_key_access_unchanged(self):
        # setup
        c = get_logged_in_client()
        url = "/accounts/profile/#key-access"

        exp_status_code = 302

        # act
        response = c.post(url, data=get_key_access_form_data())

        # test
        self.assertEqual(exp_status_code, response.status_code)
