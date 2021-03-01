# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from django.views.static import serve

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("apps.users.urls")),
    path("accounts/", include("apps.legacy.urls")),
    path("", include("cms.urls")),
    re_path(r"^sitemap\.xml$", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = (
        [re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True})]
        + staticfiles_urlpatterns()
        + urlpatterns
    )
