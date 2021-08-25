import datetime
from io import BytesIO

import bs4
from PIL import Image
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.core.files.base import File
from django.test import TestCase

from cosmos.models import News


# https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
def get_image_file(name="test.png", ext="png", size=None, color=None):
    if size is None:
        size = (50, 50)
    if color is None:
        color = (256, 0, 0)
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class NewsListViewTest(TestCase):
    url = "/news/list/"

    def setUp(self) -> None:
        News(
            title="Past public news",
            publish_date="2010-10-21",
            image=get_image_file(),
            member_only=False,
            lead="pp lead",
            content="pp content",
        ).save()
        News(
            title="Past member news",
            publish_date="2010-12-31",
            image=get_image_file(),
            member_only=True,
            lead="pp lead",
            content="pp content",
        ).save()
        News(
            title="Future public news",
            publish_date="2100-10-21",
            image=get_image_file(),
            member_only=False,
            lead="pp lead",
            content="pp content",
        ).save()
        News(
            title="Future member news",
            publish_date="2100-12-31",
            image=get_image_file(),
            member_only=True,
            lead="pp lead",
            content="pp content",
        ).save()

    def assert_news_object_view_visible(
        self, news_object: bs4.Tag, title: str, publish_date: str, can_change=False, can_delete=False
    ):
        self.assertEqual(title, news_object.find("h5", {"class": "card-title"}).contents[0])
        date = datetime.date.fromisoformat(publish_date).strftime("%b. %d, %Y")  # default date format
        self.assertEqual(f"By  - {date}", news_object.find("small", {"class": "text-muted"}).contents[0].strip())

        news = News.objects.get(title=title)

        output = news_object.find("div", {"class": "news-disabled"})
        if news.published():
            self.assertIsNone(output)
        else:
            self.assertIsNotNone(output)

        if can_change:
            self.assertEqual(f"/news/{news.pk}/update/", news_object.find_all("a", {"class": "btn p-0"})[0].get("href"))
        else:
            self.assertIsNone(news_object.find("a", {"class": "btn p-0", "href": f"/news/{news.pk}/update/"}))

        if can_delete:
            self.assertEqual(f"/news/{news.pk}/delete/", news_object.find_all("a", {"class": "btn p-0"})[1].get("href"))
        else:
            self.assertIsNone(news_object.find("a", {"class": "btn p-0", "href": f"/news/{news.pk}/delete/"}))

    def test_public_view(self):
        self.client.logout()

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="GMMGrid")
        articles = grid.find_all("div", {"class": "col"})

        self.assertEqual(1, len(articles))
        self.assert_news_object_view_visible(articles[0], "Past public news", "2010-10-21", False, False)

    def test_member_view(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="GMMGrid")
        articles = grid.find_all("div", {"class": "col"})

        self.assertEqual(2, len(articles))
        self.assert_news_object_view_visible(articles[0], "Past member news", "2010-12-31", False, False)
        self.assert_news_object_view_visible(articles[1], "Past public news", "2010-10-21", False, False)

    def test_admin_view(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="GMMGrid")
        articles = grid.find_all("div", {"class": "col"})

        self.assertEqual(4, len(articles))
        self.assert_news_object_view_visible(articles[0], "Future member news", "2100-12-31", True, True)
        self.assert_news_object_view_visible(articles[1], "Future public news", "2100-10-21", True, True)
        self.assert_news_object_view_visible(articles[2], "Past member news", "2010-12-31", True, True)
        self.assert_news_object_view_visible(articles[3], "Past public news", "2010-10-21", True, True)


class NewsUpdateViewTest(TestCase):
    def test_prefill_data_from_db(self):
        # TODO
        pass
