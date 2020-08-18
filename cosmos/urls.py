# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.static import serve

from cosmos.views import user
from cosmos.views.plugins.contact import ContactFormAjaxView
from legacy.views import legacy

admin.autodiscover()

urlpatterns = [
    # --- User focused --- #
    url(r"^accounts/register/$", user.register, name="user_register"),
    url(r"^accounts/update/$", user.update, name="user_update"),
    url(
        r"^accounts/import/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        legacy.import_user,
        name="import_user",
    ),
    # Authentication Views
    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#using-the-views
    # TODO consider manualy adding URL's to only allow password_reset or _change
    path("accounts/", include("django.contrib.auth.urls")),
    url(r"^ajax/contact$", ContactFormAjaxView.as_view(), name="ajax_contact"),
    # --- Sitemap --- #
    url(r"^sitemap\.xml$", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    url(r"^admin/", admin.site.urls),
    url(r"^", include("cms.urls")),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = (
        [url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, "show_indexes": True})]
        + staticfiles_urlpatterns()
        + urlpatterns
    )
