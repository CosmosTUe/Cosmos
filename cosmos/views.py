import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, UpdateView
from django_sendfile import sendfile

from apps.users.models import Profile
from cosmos.constants import FOUNDING_DATE
from cosmos.forms import GMMForm, GMMFormSet, GMMFormSetHelper, NewsForm, PhotoAlbumForm, PhotoObjectForm
from cosmos.models import GMM, News, PhotoAlbum, PhotoObject, Testimonial

from .settings import LOGIN_URL, SENDFILE_ROOT


def index(request):
    members = Profile.objects.count()
    nationalities = Profile.objects.values("nationality").distinct().count()
    active_years = int((datetime.date.today() - FOUNDING_DATE).days // 365.25)
    events_amount = 69  # TODO include actual event number
    if not request.user.is_authenticated:
        news_list = News.objects.filter(member_only=False, date__lte=datetime.date.today()).order_by("-date")[:3]
    else:
        news_list = News.objects.filter(date__lte=datetime.date.today()).order_by("-date")[:3]

    return render(
        request,
        "index.html",
        {
            "member_amount": members,
            "nationality_amount": nationalities,
            "active_years": active_years,
            "events_amount": events_amount,
            "news_list": news_list,
        },
    )


def error400(request, exception):
    template = loader.get_template("error_page.html")
    context = {
        "error_message": "ERROR 400: Bad request",
        "detailed_message": "Your client has issued a malformed or illegal request.",
    }
    return HttpResponse(template.render(context, request), status=400)


def error403(request, exception):
    template = loader.get_template("error_page.html")
    context = {
        "error_message": "ERROR 403: Permission denied",
        "detailed_message": "Your client does not have permission to get the requested resource from this server.",
    }
    return HttpResponse(template.render(context, request), status=403)


def error404(request, exception):
    template = loader.get_template("error_page.html")
    print(exception)
    context = {
        "error_message": "ERROR 404: Page not found",
        "detailed_message": "The requested resource could not be found on this server.",
    }
    return HttpResponse(template.render(context, request), status=404)


def error500(request):
    template = loader.get_template("error_page.html")
    context = {
        "error_message": "ERROR 500: Server error",
        "detailed_message": "The server encountered an error and could not complete your request.",
    }
    return HttpResponse(template.render(context, request), status=500)


class GMMCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = GMM
    template_name = "gmm/gmm_create.html"
    form_class = GMMForm
    success_url = None

    # Permissions
    permission_required = "cosmos.add_gmm"
    raise_exception = True

    def get_context_data(self, **kwargs):
        data = super(GMMCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["files"] = GMMFormSet(self.request.POST, self.request.FILES, instance=self.object)
            data["helper"] = GMMFormSetHelper()
        else:
            data["files"] = GMMFormSet(instance=self.object)
            data["helper"] = GMMFormSetHelper()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        files = context["files"]
        with transaction.atomic():
            self.object = form.save()
            if files.is_valid():
                files.instance = self.object
                files.save()
            else:
                return False
        return super(GMMCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("gmm-list")


class GMMUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = GMM
    template_name = "gmm/gmm_update.html"
    form_class = GMMForm
    success_url = None

    # Permissions
    permission_required = "cosmos.change_gmm"
    raise_exception = True

    def get_context_data(self, **kwargs):
        data = super(GMMUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["files"] = GMMFormSet(self.request.POST, self.request.FILES, instance=self.object)
            data["helper"] = GMMFormSetHelper()
        else:
            data["files"] = GMMFormSet(instance=self.object)
            data["helper"] = GMMFormSetHelper()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        files = context["files"]
        with transaction.atomic():
            self.object = form.save()
            if files.is_valid():
                files.instance = self.object
                files.save()
        return super(GMMUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("gmm-list")


class GMMDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = GMM
    template_name = "gmm/gmm_confirm_delete.html"
    success_url = reverse_lazy("gmm-list")

    # Permissions
    permission_required = "cosmos.delete_gmm"
    raise_exception = True


def protected_media(request, file_path):
    user = request.user

    if file_path.startswith("gmm/") and not user.is_authenticated:
        raise PermissionDenied()

    return sendfile(request, SENDFILE_ROOT + file_path)


def gmm_list(request):
    gmm_list = GMM.objects.order_by("-date").all()
    context = {
        "gmm_list": gmm_list,
    }
    return render(request, "gmm/gmm_list.html", context)


def resources(request):
    return render(request, "resources.html")


def policy(request):
    return render(request, "policy.html")


def about(request):
    testimonials = Testimonial.objects.all()
    context = {"testimonials": testimonials}
    return render(request, "about.html", context)


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")


class PhotoAlbumCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = PhotoAlbum
    template_name = "photo_album/photo_album_create.html"
    form_class = PhotoAlbumForm
    success_url = None

    # Permissions
    permission_required = "cosmos.add_photoalbum"
    raise_exception = True

    def form_valid(self, form):
        self.object = form.save()
        for img in self.request.FILES.getlist("photos"):
            PhotoObject.objects.create(album=self.object, photo=img)
        return super(PhotoAlbumCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("photo_album-list")


class PhotoAlbumDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PhotoAlbum
    template_name = "photo_album/photo_album_confirm_delete.html"
    success_url = reverse_lazy("photo_album-list")

    # Permissions
    permission_required = "cosmos.delete_photoalbum"
    raise_exception = True


class PhotoObjectDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = PhotoObject
    template_name = "photo_album/photo_object_confirm_delete.html"

    # Permissions
    permission_required = "cosmos.delete_photoobject"
    raise_exception = True

    def get_success_url(self) -> str:
        return reverse_lazy("photo_album-view", kwargs={"pk": self.get_object().album.id})


def photo_album_add_photo(request, pk):
    album = get_object_or_404(PhotoAlbum, pk=pk)

    if request.method == "POST":
        print(request.FILES)
        for img in request.FILES.getlist("photo"):
            PhotoObject.objects.create(album=album, photo=img)
        return redirect(reverse("photo_album-view", kwargs={"pk": album.id}))
    else:
        form = PhotoObjectForm()

    return render(request, "photo_album/photo_album_add_photos.html", {"form": form})


def photo_album_list(request):
    newest_album = PhotoAlbum.objects.order_by("-date")
    if not newest_album.exists():
        context = {
            "album_list": None,
            "year": datetime.datetime.now().year,
            "prev": False,
            "next": False,
        }
        return render(request, "photo_album/photo_album_list.html", context)
    else:
        newest_album = newest_album[0]
    if newest_album.date < datetime.date(newest_album.date.year, 8, 1):
        year = newest_album.date.year - 1
    else:
        year = newest_album.date.year
    return photo_album_list_year(request, year)


def photo_album_list_year(request, year):
    # Take august 1st as start of new academic year so as to include intro
    start_academic_year = datetime.datetime(year, 8, 1)
    end_academic_year = datetime.datetime(year + 1, 7, 31)
    album_list = PhotoAlbum.objects.filter(date__gte=start_academic_year, date__lte=end_academic_year).order_by("-date")

    # check prev button
    prev_test = PhotoAlbum.objects.filter(date__lte=start_academic_year)
    if prev_test:
        prev_button = True
    else:
        prev_button = False

    # check next button
    next_test = PhotoAlbum.objects.filter(date__gte=end_academic_year)
    if next_test:
        next_button = True
    else:
        next_button = False
    # TODO: check the above logic

    context = {
        "album_list": album_list,
        "year": year,
        "prev": prev_button,
        "next": next_button,
    }
    return render(request, "photo_album/photo_album_list.html", context)


def photo_album_view(request, pk):
    album = get_object_or_404(PhotoAlbum, pk=pk)
    context = {"album": album}
    return render(request, "photo_album/photo_album_view.html", context)


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
    if article.member_only and not request.user.is_authenticated:
        return redirect("%s?next=%s" % (LOGIN_URL, request.path))
    return render(request, "news/news_view.html", context)


def news_list(request):
    if not request.user.is_authenticated:
        news_list = News.objects.filter(member_only=False, date__lte=datetime.date.today()).order_by("-date")
    elif request.user.has_perm("cosmos.view_news"):
        news_list = News.objects.order_by("-date").all()
    else:
        news_list = News.objects.filter(date__lte=datetime.date.today()).order_by("-date").all()
    context = {
        "news_list": news_list,
    }
    return render(request, "news/news_list.html", context)
