from django.test import TestCase


class InstitutionTueAdminViewTest(TestCase):
    def test_success_send_stats(self):
        # setup
        url = "/admin/users/institutiontue/getstats/"
        exp_status_code = 200
        exp_content_type = "application/zip"

        # act
        response = self.client.get(url)

        # test
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_content_type, response.headers["Content-Type"])
