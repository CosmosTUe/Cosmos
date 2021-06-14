# from django.http import HttpResponse
import datetime
import random

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from apps.users.models import Profile
from cosmos.constants import FOUNDING_DATE


def index(request):
    members = Profile.objects.count()
    nationalities = Profile.objects.values("nationality").distinct().count()
    active_years = int((datetime.date.today() - FOUNDING_DATE).days // 365.25)
    events_amount = random.randint(0, 69)  # TODO include actual event number

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
