from .gmm_view import GMMViewsTestAdminLoggedIn, GMMViewsTestLoggedOut, GMMViewsTestMemberLoggedIn
from .news import NewsViewTest, NewsListViewTest, NewsCreateViewTest, NewsDeleteViewTest, NewsUpdateViewTest
from .photo_view import (
    PhotoAlbumListViewTest,
    PhotoAlbumCreateViewTest,
    PhotoAlbumDeleteViewTest,
    PhotoAlbumUpdateViewTest,
    PhotoAlbumAddPhotoViewTest,
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
