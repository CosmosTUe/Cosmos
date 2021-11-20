from django.test import TestCase

from apps.core.forms.gmm import GMMForm


def generate_form(name, date):
    return GMMForm(data={"name": name, "date": date})


class GMMFormTest(TestCase):
    def test_empty_form(self):
        # setup

        # act
        form = generate_form("", "")

        # test
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("name", "required"))
        self.assertTrue(form.has_error("date", "required"))

    def test_whitespace_only_name(self):
        # setup
        name = " " * 10
        date = "2010-10-21"

        # act
        form = generate_form(name, date)

        # test
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("name", "required"))
        self.assertFalse(form.has_error("date"))

    def test_invalid_date_format(self):
        # setup
        name = "myGMM"
        date = "2010-21-10"

        # act
        form = generate_form(name, date)

        # test
        self.assertFalse(form.is_valid())
        self.assertFalse(form.has_error("name", "invalid"))
        self.assertTrue(form.has_error("date", "invalid"))
