from __future__ import absolute_import, print_function, unicode_literals

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from apps.core.views.core import about, index, resources, terms
from apps.core.views.gmm import GMMCreate, GMMDelete, GMMUpdate, gmm_list
from apps.core.views.internal import (
    InternalDocumentCreate,
    InternalDocumentDelete,
    InternalDocumentUpdate,
    internal_list,
)
from apps.core.views.misc import protected_media, update_door_status
from apps.core.views.news import NewsCreate, NewsDelete, NewsUpdate, news_list, news_view
from apps.core.views.photos import (
    PhotoAlbumCreate,
    PhotoAlbumDelete,
    PhotoAlbumUpdate,
    PhotoObjectDelete,
    photo_album_add_photo,
    photo_album_list,
    photo_album_list_year,
    photo_album_view,
)

app_name = "cosmos_core"

urlpatterns = [
    # Core views
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("resources/", resources, name="resources"),
    path("terms/", terms, name="terms"),
    # GMM views
    path("gmm/add/", GMMCreate.as_view(), name="gmm-create"),
    path("gmm/list/", gmm_list, name="gmm-list"),
    path("gmm/<int:pk>/update", GMMUpdate.as_view(), name="gmm-update"),
    path("gmm/<int:pk>/delete", GMMDelete.as_view(), name="gmm-delete"),
    # Internal Documents views
    path("internal/add/", InternalDocumentCreate.as_view(), name="internal-create"),
    path("internal/list/", internal_list, name="internal-list"),
    path("internal/<int:pk>/update", InternalDocumentUpdate.as_view(), name="internal-update"),
    path("internal/<int:pk>/delete", InternalDocumentDelete.as_view(), name="internal-delete"),
    # Photos views
    path("photos/create/", PhotoAlbumCreate.as_view(), name="photo_album-create"),
    path("photos/list/", photo_album_list, name="photo_album-list"),
    path("photos/list/<int:year>/", photo_album_list_year, name="photo_album-list_year"),
    path("photos/<int:pk>/", photo_album_view, name="photo_album-view"),
    path("photos/<int:pk>/add/", photo_album_add_photo, name="photo_album-add_photos"),
    path("photos/<int:pk>/delete/", PhotoAlbumDelete.as_view(), name="photo_album-delete"),
    path("photos/<int:pk>/update/", PhotoAlbumUpdate.as_view(), name="photo_album-update"),
    path("photos/delete_single/<int:pk>/", PhotoObjectDelete.as_view(), name="photo_object-delete"),
    # News views
    path("news/add/", NewsCreate.as_view(), name="news-create"),
    path("news/list/", news_list, name="news-list"),
    path("news/<int:pk>/", news_view, name="news-view"),
    path("news/<int:pk>/update/", NewsUpdate.as_view(), name="news-update"),
    path("news/<int:pk>/delete/", NewsDelete.as_view(), name="news-delete"),
    # Misc views
    path("media/<path:file_path>", protected_media, name="protected-media"),
    path("door-status", update_door_status, name="update-door-status"),
]

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
