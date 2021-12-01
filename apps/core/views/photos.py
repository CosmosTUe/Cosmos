import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.core.forms.photos import PhotoAlbumForm, PhotoAlbumUpdateForm, PhotoObjectForm
from apps.core.models.photos import PhotoAlbum, PhotoObject
from apps.core.views.errors import error403


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
        return reverse_lazy("cosmos_core:photo_album-list")


class PhotoAlbumUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = PhotoAlbum
    template_name = "photo_album/photo_album_update.html"
    form_class = PhotoAlbumUpdateForm
    success_url = None

    # permissions
    permission_required = "cosmos.change_photoalbum"
    raise_exception = True


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
        return reverse_lazy("cosmos_core:photo_album-view", kwargs={"pk": self.get_object().album.id})


def photo_album_add_photo(request, pk):
    if not request.user.has_perm("cosmos.change_photoalbum"):
        return error403(request, None)

    album = get_object_or_404(PhotoAlbum, pk=pk)

    if request.method == "POST":
        print(request.FILES)
        for img in request.FILES.getlist("photo"):
            PhotoObject.objects.create(album=album, photo=img)
        return redirect(reverse("cosmos_core:photo_album-view", kwargs={"pk": album.id}))
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
