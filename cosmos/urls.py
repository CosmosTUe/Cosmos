# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.static import serve
from cosmos.views import user

admin.autodiscover()

urlpatterns = [
    # --- User focused --- #
    url(r"^accounts/register/$", user.register, name="user_register"),
    url(r"^accounts/update/$", user.update, name="user_update"),
    # Authentication Views
    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#using-the-views
    # TODO consider manualy adding URL's to only allow password_reset or _change
    path("accounts/", include("django.contrib.auth.urls")),
    # --- Sitemap --- #
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
]

urlpatterns += i18n_patterns(url(r"^admin/", admin.site.urls), url(r"^", include("cms.urls")),)  # NOQA

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = (
        [url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True})]
        + staticfiles_urlpatterns()
        + urlpatterns
    )
