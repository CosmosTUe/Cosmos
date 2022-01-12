from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.core.forms.internal import InternalDocumentForm
from apps.core.models.internal import InternalDocument


class InternalDocumentCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = InternalDocument
    template_name = "internal/internal_create.html"
    form_class = InternalDocumentForm
    success_url = reverse_lazy("cosmos_core:internal-list")

    # Permissions
    permission_required = "cosmos.add_internaldocument"
    raise_exception = True


class InternalDocumentUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = InternalDocument
    template_name = "internal/internal_update.html"
    form_class = InternalDocumentForm
    success_url = reverse_lazy("cosmos_core:internal-list")

    # Permissions
    permission_required = "cosmos.change_internaldocument"
    raise_exception = True


class InternalDocumentDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = InternalDocument
    template_name = "internal/internal_confirm_delete.html"
    success_url = reverse_lazy("cosmos_core:internal-list")

    # Permissions
    permission_required = "cosmos.delete_internaldocument"
    raise_exception = True


def internal_list(request):
    internal_list = InternalDocument.objects.order_by("name").all()
    context = {
        "internal_list": internal_list,
    }
    return render(request, "internal/internal_list.html", context)
