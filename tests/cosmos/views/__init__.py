from .gmm_view import FileObjectStrTest, GMMViewsTestAdminLoggedIn, GMMViewsTestLoggedOut, GMMViewsTestMemberLoggedIn
from .index import DoorSensorTest
from .logout import LogoutTest
from .news import NewsCreateViewTest, NewsDeleteViewTest, NewsListViewTest, NewsUpdateViewTest, NewsViewTest
from .permissions import (
    CopyOldPermissionsMigrationTest,
    CurrentPermissionNamesTest,
    RemoveStaleContentTypesMigrationTest,
)
from .photo_view import (
    PhotoAlbumAddPhotoViewTest,
    PhotoAlbumCreateViewTest,
    PhotoAlbumDeleteViewTest,
    PhotoAlbumListViewTest,
    PhotoAlbumUpdateViewTest,
    PhotoAlbumViewsTest,
)
from .sitemap import SitemapTest

__all__ = [
    "CurrentPermissionNamesTest",
    "CopyOldPermissionsMigrationTest",
    "RemoveStaleContentTypesMigrationTest",
    "LogoutTest",
    "GMMViewsTestLoggedOut",
    "GMMViewsTestMemberLoggedIn",
    "GMMViewsTestAdminLoggedIn",
    "FileObjectStrTest",
    "NewsViewTest",
    "NewsListViewTest",
    "NewsCreateViewTest",
    "NewsDeleteViewTest",
    "NewsUpdateViewTest",
    "PhotoAlbumAddPhotoViewTest",
    "PhotoAlbumViewsTest",
    "PhotoAlbumUpdateViewTest",
    "PhotoAlbumDeleteViewTest",
    "PhotoAlbumCreateViewTest",
    "PhotoAlbumListViewTest",
    "DoorSensorTest",
    "SitemapTest",
]
