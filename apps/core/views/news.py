import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.core.forms.news import NewsForm
from apps.core.models.news import News
from apps.core.views.errors import error403
from cosmos.settings import LOGIN_URL


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    template_name = "news/news_create.html"
    form_class = NewsForm
    success_url = None

    # Permissions
    permission_required = "cosmos.add_news"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("news-list")


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    template_name = "news/news_update.html"
    form_class = NewsForm
    success_url = None

    # Permissions
    permission_required = "cosmos.change_news"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("news-list")


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = "news/news_confirm_delete.html"
    success_url = reverse_lazy("news-list")

    # Permissions
    permission_required = "cosmos.delete_news"
    raise_exception = True


def news_view(request, pk):
    article = get_object_or_404(News, pk=pk)
    context = {"article": article}
    if not article.published() and not request.user.has_perms(["cosmos.change_news", "cosmos.delete_news"]):
        return error403(request, None)
    if article.member_only and not request.user.is_authenticated:
        return redirect("%s?next=%s" % (LOGIN_URL, request.path))
    return render(request, "news/news_view.html", context)


def news_list(request):
    if not request.user.is_authenticated:
        news_list = News.objects.filter(member_only=False, publish_date__lte=datetime.date.today()).order_by(
            "-publish_date"
        )
    elif request.user.has_perm("cosmos.view_news"):
        news_list = News.objects.order_by("-publish_date").all()
    else:
        news_list = News.objects.filter(publish_date__lte=datetime.date.today()).order_by("-publish_date").all()
    context = {
        "news_list": news_list,
    }
    return render(request, "news/news_list.html", context)
