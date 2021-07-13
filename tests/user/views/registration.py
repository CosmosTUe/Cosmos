from tests.user.views.wizard_helper import WizardViewTestCase


class RegistrationViewTest(WizardViewTestCase):
    def test_success_tue(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"

        # act
        response = self.get_wizard_response(
            url,
            {
                "register_user": {
                    "first_name": "Tosti",
                    "last_name": "Broodjes",
                    "username": "tosti@student.tue.nl",
                    "email": "tosti@gmail.com",
                    "password1": "ikbeneenbrood",
                    "password2": "ikbeneenbrood",
                    "nationality": "Dutch",
                    "terms_confirmed": "on",
                    "subscribed_newsletter": "on",
                },
                "register_tue": {
                    "department": "Mathematics and Computer Science",
                    "program": "Bachelor",
                },
            },
        )

        # test
        self.assertEqual(done_url, response.url)

    def test_success_fontys(self):
        # setup
        url = "/accounts/register/"
        done_url = "/accounts/register/done/"

        # act
        response = self.get_wizard_response(
            url,
            {
                "register_user": {
                    "first_name": "Tosti",
                    "last_name": "Broodjes",
                    "username": "tosti@fontys.nl",
                    "email": "tosti@gmail.com",
                    "password1": "ikbeneenbrood",
                    "password2": "ikbeneenbrood",
                    "nationality": "Dutch",
                    "terms_confirmed": "on",
                    "subscribed_newsletter": "on",
                },
                "register_fontys": {
                    "study": "test",  # TODO fix Fontys studies
                },
            },
        )

        # test
        self.assertEqual(done_url, response.url)
