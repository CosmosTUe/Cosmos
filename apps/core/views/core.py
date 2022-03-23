import datetime
import os

from django.shortcuts import render

from apps.core.constants import FOUNDING_DATE
from apps.core.models.core import Partner, Testimonial
from apps.core.models.news import News
from apps.users.models import Board, Profile


def index(request):
    members = Profile.objects.count()
    nationalities = Profile.objects.values("nationality").distinct().count()
    active_years = int((datetime.date.today() - FOUNDING_DATE).days // 365.25)
    events_amount = "20+"
    partners = Partner.objects.all().order_by("?")

    if os.path.exists("/tmp/door-open"):
        door_status = 1
    else:
        door_status = 0
    if not request.user.is_authenticated:
        news_list = News.objects.filter(member_only=False, publish_date__lte=datetime.date.today()).order_by(
            "-publish_date"
        )[:3]
    else:
        news_list = News.objects.filter(publish_date__lte=datetime.date.today()).order_by("-publish_date")[:3]

    return render(
        request,
        "index.html",
        {
            "member_amount": members,
            "nationality_amount": nationalities,
            "active_years": active_years,
            "events_amount": events_amount,
            "news_list": news_list,
            "partners": partners,
            "door_status": door_status,
        },
    )


def resources(request):
    return render(request, "resources.html")


def about(request):
    testimonials = Testimonial.objects.all()
    boards = Board.objects.order_by("-period_from")
    if boards:
        board = boards[0]
    else:
        board = None
    context = {"testimonials": testimonials, "board": board}
    return render(request, "about.html", context)


def terms(request):
    return render(request, "terms.html")


def merch(request):
    return render(request, "merch.html")
