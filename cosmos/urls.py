from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path

from apps.users.views import board_overview, committee_overview, committee_subpage

admin.autodiscover()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),  # django-oauth-toolkit
    path("accounts/", include("apps.users.urls")),
    path("events/", include("apps.events.urls")),
    path("boards/", board_overview, name="boards_overview"),
    path("committees/", committee_overview, name="committee_overview"),
    path("committees/<slug>/", committee_subpage, name="committee_subpage"),
    path("", include("apps.core.urls")),
    re_path(r"^sitemap\.xml$", sitemap),
]

handler400 = "apps.core.views.errors.error400"
handler403 = "apps.core.views.errors.error403"
handler404 = "apps.core.views.errors.error404"
handler500 = "apps.core.views.errors.error500"

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
