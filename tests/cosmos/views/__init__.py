from .gmm_view import GMMViewsTestAdminLoggedIn, GMMViewsTestLoggedOut, GMMViewsTestMemberLoggedIn
from .news import NewsViewTest, NewsListViewTest, NewsCreateViewTest, NewsDeleteViewTest, NewsUpdateViewTest
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
