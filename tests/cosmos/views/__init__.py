from .gmm_view import GMMViewsTestAdminLoggedIn, GMMViewsTestLoggedOut, GMMViewsTestMemberLoggedIn
from .news import NewsCreateViewTest, NewsDeleteViewTest, NewsListViewTest, NewsUpdateViewTest, NewsViewTest
from .photo_view import (
    PhotoAlbumAddPhotoViewTest,
    PhotoAlbumCreateViewTest,
    PhotoAlbumDeleteViewTest,
    PhotoAlbumListViewTest,
    PhotoAlbumUpdateViewTest,
    PhotoAlbumViewsTest,
)

__all__ = [
    "GMMViewsTestLoggedOut",
    "GMMViewsTestMemberLoggedIn",
    "GMMViewsTestAdminLoggedIn",
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
]
