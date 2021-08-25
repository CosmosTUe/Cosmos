from django.test import TestCase

from cosmos.forms import NewsForm


def generate_form(title="", publish_date="", image="", member_only=False, lead="", content=""):
    return NewsForm(
        data={
            "title": title,
            "publish_date": publish_date,
            "image": image,
            "member_only": member_only,
            "lead": lead,
            "content": content,
        }
    )


class NewsFormTest(TestCase):
    def test_empty_form(self):
        form = generate_form()

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error("title", "required"))
        self.assertTrue(form.has_error("publish_date", "required"))
        self.assertTrue(form.has_error("image", "required"))
        self.assertFalse(form.has_error("member_only", "required"))
        self.assertFalse(form.has_error("lead", "required"))
        self.assertTrue(form.has_error("content", "required"))
