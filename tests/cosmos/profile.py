from django.contrib.auth.models import User
from django.test import TestCase

from apps.users.forms import ProfileUpdateForm
from apps.users.models import Profile


def generate_tue_user(
    username="tosti@student.tue.nl",
    email="tosti@gmail.com",
    password="ikbeneenbrood",
    nationality="Dutch",
    subscribed_newsletter=False,
    department="Electrical Engineering",
    program="Bachelor",
):
    user = User.objects.create_user(username=username, email=email, password=password)
    profile = Profile.objects.create(
        user=user,
        nationality=nationality,
        terms_confirmed=True,
        subscribed_newsletter=subscribed_newsletter,
    )
    institution = profile.institution
    institution.department = department
    institution.program = program
    institution.save()
    return user


class ProfileUpdateFormTest(TestCase):
    def generate_form(self):
        pass

    def setUp(self) -> None:
        self.user = generate_tue_user()

    def test_prefill_data_from_db(self):
        # setup

        # act
        form = ProfileUpdateForm(instance=self.user)

        # test
        self.assertEqual(form["username"].initial, "tosti@student.tue.nl")
        self.assertEqual(form["email"].initial, "tosti@gmail.com")
        self.assertEqual(form["nationality"].initial, "Dutch")
        self.assertEqual(form["department"].initial, "Electrical Engineering")
        self.assertEqual(form["program"].initial, "Bachelor")
        self.assertEqual(form["study"].initial, None)
