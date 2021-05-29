from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from cosmos.models import GMM


def index(request):
    return render(request, "index.html")


def resources(request):
    # TODO: sort by date, newest first
    gmm_list = GMM.objects.all()
    template = loader.get_template("resources.html")
    context = {
        "gmm_list": gmm_list,
    }
    return HttpResponse(template.render(context, request))
