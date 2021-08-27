from .gmm_view import GMMViewsTestAdminLoggedIn, GMMViewsTestLoggedOut, GMMViewsTestMemberLoggedIn
from .news import NewsCreateViewTest, NewsDeleteViewTest, NewsListViewTest, NewsUpdateViewTest, NewsViewTest
from .photo_view import PhotoListViewTest

__all__ = [
    "GMMViewsTestLoggedOut",
    "GMMViewsTestMemberLoggedIn",
    "GMMViewsTestAdminLoggedIn",
    "NewsViewTest",
    "NewsListViewTest",
    "NewsCreateViewTest",
    "NewsDeleteViewTest",
    "NewsUpdateViewTest",
    "PhotoListViewTest",
]
