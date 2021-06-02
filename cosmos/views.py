from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.db import transaction

from cosmos.models import GMM
from cosmos.forms import GMMForm, GMMFormSet, GMMFormSetHelper


def index(request):
    return render(request, "index.html")


def resources(request):
    gmm_list = GMM.objects.order_by("-date").all()
    template = loader.get_template("resources.html")
    context = {
        "gmm_list": gmm_list,
    }
    return HttpResponse(template.render(context, request))


class GMMCreate(CreateView):
    model = GMM
    template_name = "cosmos/gmm_form.html"
    form_class = GMMForm
    success_url = None

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


class GMMUpdate(UpdateView):
    model = GMM
    template_name = "cosmos/gmm_form.html"
    form_class = GMMForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(GMMUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data["files"] = GMMFormSet(self.request.POST, self.request.FILES, instance=self.object)
            print(self.request.POST | self.request.FILES)
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


class GMMDelete(DeleteView):
#    form_class = GMMDeleteForm
    model = GMM
    success_url = reverse_lazy("resources")
