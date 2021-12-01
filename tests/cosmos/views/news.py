import datetime

import bs4
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.test import TestCase

from apps.core.models.news import News
from tests.cosmos.helpers import get_image_file


class NewsCreateViewTest(TestCase):
    url = "/news/add/"

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)


class NewsViewTest(TestCase):
    def setUp(self) -> None:
        self.pp = News(
            title="Past public news",
            publish_date="2010-10-21",
            image=get_image_file(),
            member_only=False,
            lead="pp lead",
            content="pp content",
        )
        self.pp.save()
        self.pm = News(
            title="Past member news",
            publish_date="2010-12-31",
            image=get_image_file(),
            member_only=True,
            lead="pp lead",
            content="pp content",
        )
        self.pm.save()
        self.fp = News(
            title="Future public news",
            publish_date="2100-10-21",
            image=get_image_file(),
            member_only=False,
            lead="pp lead",
            content="pp content",
        )
        self.fp.save()
        self.fm = News(
            title="Future member news",
            publish_date="2100-12-31",
            image=get_image_file(),
            member_only=True,
            lead="pp lead",
            content="pp content",
        )
        self.fm.save()

    def tearDown(self) -> None:
        News.objects.all().delete()

    def assert_news_view_visible(self, pk):
        url = f"/news/{pk}/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def assert_news_not_found(self, pk):
        url = f"/news/{pk}/"
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def assert_news_member_only(self, pk):
        url = f"/news/{pk}/"
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def assert_news_forbidden(self, pk):
        url = f"/news/{pk}/"
        response = self.client.get(url)
        self.assertEqual(403, response.status_code)

    def test_public_view(self):
        self.client.logout()

        self.assert_news_view_visible(self.pp.pk)
        self.assert_news_member_only(self.pm.pk)
        self.assert_news_forbidden(self.fp.pk)
        self.assert_news_forbidden(self.fm.pk)
        self.assert_news_not_found(500)  # invalid news pk

    def test_member_view(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        self.assert_news_view_visible(self.pp.pk)
        self.assert_news_view_visible(self.pm.pk)
        self.assert_news_forbidden(self.fp.pk)
        self.assert_news_forbidden(self.fm.pk)
        self.assert_news_not_found(500)  # invalid news pk

    def test_admin_view(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        self.assert_news_view_visible(self.pp.pk)
        self.assert_news_view_visible(self.pm.pk)
        self.assert_news_view_visible(self.fp.pk)
        self.assert_news_view_visible(self.fm.pk)
        self.assert_news_not_found(500)  # invalid news pk


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

    def tearDown(self) -> None:
        News.objects.all().delete()

    def assert_news_card_visible(
        self, news_object: bs4.Tag, title: str, publish_date: str, can_change=False, can_delete=False
    ):
        self.assertEqual(title, news_object.find("h5", {"class": "card-title"}).contents[0])
        date = datetime.date.fromisoformat(publish_date).strftime("%d %b %Y")  # default date format
        self.assertEqual(f"By  - {date}", news_object.find("small", {"class": "text-muted"}).contents[0].strip())

        news = News.objects.get(title=title)

        output = news_object.find("div", {"class": "news-disabled"})
        if news.published():
            self.assertIsNone(output)
        else:
            self.assertIsNotNone(output)

        if can_change:
            self.assertEqual(
                f"/news/{news.pk}/update/",
                news_object.find_all("a", {"class": "btn p-0 btn-over-stretched"})[0].get("href"),
            )
        else:
            self.assertIsNone(news_object.find("a", {"class": "btn p-0", "href": f"/news/{news.pk}/update/"}))

        if can_delete:
            self.assertEqual(
                f"/news/{news.pk}/delete/",
                news_object.find_all("a", {"class": "btn p-0 btn-over-stretched"})[1].get("href"),
            )
        else:
            self.assertIsNone(news_object.find("a", {"class": "btn p-0", "href": f"/news/{news.pk}/delete/"}))

    def test_public_view(self):
        self.client.logout()

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="NewsGrid")
        articles = grid.find_all("div", {"class": "col"})

        self.assertEqual(1, len(articles))
        self.assert_news_card_visible(articles[0], "Past public news", "2010-10-21", False, False)

    def test_member_view(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="NewsGrid")
        articles = grid.find_all("div", {"class": "col"})

        self.assertEqual(2, len(articles))
        self.assert_news_card_visible(articles[0], "Past member news", "2010-12-31", False, False)
        self.assert_news_card_visible(articles[1], "Past public news", "2010-10-21", False, False)

    def test_admin_view(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        html_parser = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
        grid = html_parser.find("div", id="NewsGrid")
        articles = grid.find_all("div", {"class": "col"})

        self.assertEqual(4, len(articles))
        self.assert_news_card_visible(articles[0], "Future member news", "2100-12-31", True, True)
        self.assert_news_card_visible(articles[1], "Future public news", "2100-10-21", True, True)
        self.assert_news_card_visible(articles[2], "Past member news", "2010-12-31", True, True)
        self.assert_news_card_visible(articles[3], "Past public news", "2010-10-21", True, True)


class NewsUpdateViewTest(TestCase):
    url = "/news/1/update/"

    def setUp(self) -> None:
        News(
            pk=1,
            title="Past public news",
            publish_date="2010-10-21",
            image=get_image_file(),
            member_only=False,
            lead="pp lead",
            content="pp content",
        ).save()

    def tearDown(self) -> None:
        News.objects.all().delete()

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)


class NewsDeleteViewTest(TestCase):
    url = "/news/1/delete/"

    def setUp(self) -> None:
        News(
            pk=1,
            title="Past public news",
            publish_date="2010-10-21",
            image=get_image_file(),
            member_only=False,
            lead="pp lead",
            content="pp content",
        ).save()

    def tearDown(self) -> None:
        News.objects.all().delete()

    def test_forbidden_for_public(self):
        self.client.logout()

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_forbidden_for_members(self):
        User.objects.create_user(username="tosti@student.tue.nl", email="tosti@cosmostue.nl", password="ikbeneenbrood")
        self.client.login(username="tosti@student.tue.nl", password="ikbeneenbrood")

        response = self.client.get(self.url)

        self.assertEqual(403, response.status_code)

    def test_accessible_for_admins(self):
        User.objects.create_superuser(
            username="admin@student.tue.nl", email="admin@cosmostue.nl", password="adminsecret"
        )
        self.client.login(username="admin@student.tue.nl", password="adminsecret")

        response = self.client.get(self.url)

        self.assertEqual(200, response.status_code)
