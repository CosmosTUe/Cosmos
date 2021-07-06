# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path

import cosmos.views
from apps.users.views import board_overview, committee_overview, committee_subpage

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),  # django-oauth-toolkit
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/", include("apps.users.urls")),
    path("boards/", board_overview, name="boards_overview"),
    path("committees/", committee_overview, name="committee_overview"),
    path("committees/<slug>/", committee_subpage, name="committee_subpage"),
    re_path(r"^sitemap\.xml$", sitemap),
    path("", cosmos.views.index, name="index"),
    path("about/", cosmos.views.about, name="about"),
    path("resources/", cosmos.views.resources, name="resources"),
    path("gmm/add/", cosmos.views.GMMCreate.as_view(), name="gmm-create"),
    path("gmm/<int:pk>/", cosmos.views.GMMUpdate.as_view(), name="gmm-update"),
    path("gmm/<int:pk>/delete", cosmos.views.GMMDelete.as_view(), name="gmm-delete"),
    path("media/<path:file_path>", cosmos.views.protected_media, name="protected-media"),
    path("privacy/", cosmos.views.privacy, name="privacy-policy"),
    path("terms/", cosmos.views.terms, name="terms"),
]

handler400 = "cosmos.views.error400"
handler403 = "cosmos.views.error403"
handler404 = "cosmos.views.error404"
handler500 = "cosmos.views.error500"

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
