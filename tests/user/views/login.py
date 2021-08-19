from bs4 import BeautifulSoup
from django.test import TestCase


class LoginViewTest(TestCase):
    def test_correct_field_labels(self):
        # setup
        url = "/accounts/login/"

        # act
        response = self.client.get(url)

        # test
        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        labels = html_parser.find_all("label")
        self.assertEqual(labels[0].text.strip(), "Institutional Email")
        self.assertEqual(labels[1].text.strip(), "Password")
        self.assertEqual(labels[2].text.strip(), "Remember me")
