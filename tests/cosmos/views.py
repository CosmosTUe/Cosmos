from django.test import TestCase


class PhotoListViewTest(TestCase):
    def test_success_blank_db(self):
        # setup
        url = "/photos/list/"

        exp_status_code = 200

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(exp_status_code, response.status_code)
