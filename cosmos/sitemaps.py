import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.core.models import News
from apps.users.models import Committee


class StaticViewSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return [
            "cosmos_core:index",
            "cosmos_core:about",
            "boards_overview",
            "committee_overview",
            "cosmos_core:news-list",
            "cosmos_events:events-archive",
            "cosmos_core:merch",
            "cosmos_core:resources",
            "cosmos_core:wellbeing",
            "cosmos_core:terms",
        ]

    def location(self, item):
        return reverse(item)


class CommitteeSitemap(Sitemap):
    protocol = "https"

    def items(self):
        # hidden committees stay reachable through their link but are left out of listings
        return Committee.objects.filter(hidden=False).order_by("slug")

    def location(self, committee):
        return reverse("committee_subpage", args=[committee.slug])


class NewsSitemap(Sitemap):
    protocol = "https"

    def items(self):
        # the same articles an anonymous visitor sees in the news list
        return News.objects.filter(member_only=False, publish_date__lte=datetime.date.today()).order_by("-publish_date")

    def location(self, article):
        return reverse("cosmos_core:news-view", args=[article.pk])

    def lastmod(self, article):
        return article.publish_date


SITEMAPS = {"static": StaticViewSitemap, "committees": CommitteeSitemap, "news": NewsSitemap}
