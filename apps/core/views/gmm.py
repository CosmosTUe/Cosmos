from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.core.forms.gmm import GMMForm, GMMFormSet, GMMFormSetHelper
from apps.core.models.gmm import GMM


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
        return reverse_lazy("cosmos_core:gmm-list")


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
        return reverse_lazy("cosmos_core:gmm-list")


class GMMDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = GMM
    template_name = "gmm/gmm_confirm_delete.html"
    success_url = reverse_lazy("cosmos_core:gmm-list")

    # Permissions
    permission_required = "cosmos.delete_gmm"
    raise_exception = True


def gmm_list(request):
    gmm_list = GMM.objects.order_by("-date").all()
    context = {
        "gmm_list": gmm_list,
    }
    return render(request, "gmm/gmm_list.html", context)
