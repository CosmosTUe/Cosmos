import datetime

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from cosmos.forms import NewsForm
from cosmos.models import News
from tests.cosmos.views.news import get_image_file


def generate_form(title="", publish_date="", image: File = None, member_only=False, lead="", content=""):
    files = {}
    if image is not None:
        files["image"] = SimpleUploadedFile(image.name, image.read())
    return NewsForm(
        data={
            "title": title,
            "publish_date": publish_date,
            "member_only": member_only,
            "lead": lead,
            "content": content,
        },
        files=files,
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

    def test_past_news_is_published(self):
        form = generate_form(
            title="Past public news",
            publish_date="2010-10-21",
            image=get_image_file(),
            lead="pp lead",
            content="pp content",
        )

        self.assertTrue(form.is_valid())
        form.save()

        news = News.objects.get(title="Past public news")
        self.assertEqual("Past public news", news.title)
        self.assertEqual(datetime.date(2010, 10, 21), news.publish_date)
        self.assertEqual("pp lead", news.lead)
        self.assertEqual("pp content", news.content)
        self.assertTrue(news.published())

    def test_future_news_is_not_published(self):
        form = generate_form(
            title="Past public news",
            publish_date="2100-10-21",
            image=get_image_file(),
            lead="pp lead",
            content="pp content",
        )

        self.assertTrue(form.is_valid())
        form.save()

        news = News.objects.get(title="Past public news")
        self.assertEqual("Past public news", news.title)
        self.assertEqual(datetime.date(2100, 10, 21), news.publish_date)
        self.assertEqual("pp lead", news.lead)
        self.assertEqual("pp content", news.content)
        self.assertFalse(news.published())
