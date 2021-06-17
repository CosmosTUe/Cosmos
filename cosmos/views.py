import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_sendfile import sendfile

from apps.users.models import Profile
from cosmos.constants import FOUNDING_DATE
from cosmos.forms import GMMForm, GMMFormSet, GMMFormSetHelper
from cosmos.models import GMM

from .settings import SENDFILE_ROOT


def index(request):
    members = Profile.objects.count()
    nationalities = Profile.objects.values("nationality").distinct().count()
    active_years = int((datetime.date.today() - FOUNDING_DATE).days // 365.25)
    events_amount = 69  # TODO include actual event number

    return render(
        request,
        "index.html",
        {
            "member_amount": members,
            "nationality_amount": nationalities,
            "active_years": active_years,
            "events_amount": events_amount,
        },
    )


def error400(request, exception):
    template = loader.get_template("error_page.html")
    context = {
        "error_message": "ERROR 400: Bad request",
        "detailed_message": "Your client has issued a malformed or illegal request.",
    }
    return HttpResponse(template.render(context, request))


def error403(request, exception):
    template = loader.get_template("error_page.html")
    context = {
        "error_message": "ERROR 403: Permission denied",
        "detailed_message": "Your client does not have permission to get the requested resource from this server.",
    }
    return HttpResponse(template.render(context, request))


def error404(request, exception):
    template = loader.get_template("error_page.html")
    print(exception)
    context = {
        "error_message": "ERROR 404: Page not found",
        "detailed_message": "The requested resource could not be found on this server.",
    }
    return HttpResponse(template.render(context, request))


def error500(request):
    template = loader.get_template("error_page.html")
    context = {
        "error_message": "ERROR 500: Server error",
        "detailed_message": "The server encountered an error and could not complete your request.",
    }
    return HttpResponse(template.render(context, request))


def resources(request):
    gmm_list = GMM.objects.order_by("-date").all()
    template = loader.get_template("resources.html")
    context = {
        "gmm_list": gmm_list,
    }
    return HttpResponse(template.render(context, request))


class GMMCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = GMM
    template_name = "gmm/gmm_create.html"
    form_class = GMMForm
    success_url = None

    # Permissions
    permission_required = "cosmos.gmm_add"
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

    def get_succes_url(self):
        return reverse_lazy("resources")


class GMMUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = GMM
    template_name = "gmm/gmm_update.html"
    form_class = GMMForm
    success_url = None

    # Permissions
    permission_required = "cosmos.gmm_update"
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

    def get_succes_url(self):
        return reverse_lazy("resources")


class GMMDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = GMM
    template_name = "gmm/gmm_confirm_delete.html"
    success_url = reverse_lazy("resources")

    # Permissions
    permission_required = "cosmos.gmm_delete"
    raise_exception = True


def protected_media(request, file_path):
    user = request.user

    if file_path.startswith("gmm/") and not user.is_authenticated:
        raise PermissionDenied()

    return sendfile(request, SENDFILE_ROOT + file_path)
