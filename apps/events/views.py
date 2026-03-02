import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView
from django_ical.views import ICalFeed

from apps.core.models import News
from apps.events.forms import EventForm
from apps.events.models import Event

PAST_EVENTS_PAGE_SIZE = 20


def events_list(request):
    now = timezone.now()

    if request.user.is_authenticated:
        upcoming_events = Event.objects.order_by("start_date_time").filter(end_date_time__gte=now)
        past_events = Event.objects.order_by("-start_date_time").filter(end_date_time__lte=now)
    else:
        upcoming_events = (
            Event.objects.filter(member_only=False).order_by("start_date_time").filter(end_date_time__gte=now)
        )
        past_events = (
            Event.objects.filter(member_only=False).order_by("-start_date_time").filter(end_date_time__lte=now)
        )

    paginator = Paginator(past_events, PAST_EVENTS_PAGE_SIZE)
    first_page = paginator.page(1)

    context = {
        "events_list": upcoming_events,
        "events_list_past": first_page.object_list,
        "past_has_next": first_page.has_next(),
    }
    return render(request, "events/events_list.html", context)


def past_events_page(request):
    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        raise Http404()

    now = timezone.now()

    past_events = Event.objects.filter(
        end_date_time__lte=now,
        member_only=False if not request.user.is_authenticated else None,
    ).order_by("-start_date_time")

    paginator = Paginator(past_events, PAST_EVENTS_PAGE_SIZE)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({"html": "", "has_next": False})

    html = render_to_string(
        "events/_past_events_cards.html",
        {"events_list_past": page_obj.object_list},
        request=request,
    )

    return JsonResponse(
        {
            "html": html,
            "has_next": page_obj.has_next(),
        }
    )


def event_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}
    if event.member_only and not request.user.is_authenticated:
        raise PermissionDenied()
    return render(request, "events/event_view.html", context)


def events_archive(request):
    if request.user.is_authenticated:
        events_list = (
            Event.objects.order_by("-start_date_time").filter(end_date_time__lt=datetime.datetime.today()).all()
        )
    else:
        events_list = (
            Event.objects.filter(member_only=False)
            .order_by("-start_date_time")
            .filter(end_date_time__lt=datetime.datetime.today())
        )
    context = {
        "events_list": events_list,
    }
    return render(request, "events/events_archive.html", context)


def event_carousel(request):
    event_list = Event.objects.order_by("start_date_time").filter(end_date_time__gt=datetime.datetime.today()).all()
    news_list = News.objects.order_by("publish_date").filter(
        publish_date__gt=datetime.datetime.today() - datetime.timedelta(days=31 * 2)
    )[:3]

    context = {
        "event_list": event_list,
        "news_list": news_list,
    }
    return render(request, "events/event_carousel.html", context)


class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = "events/event_create.html"
    form_class = EventForm
    success_url = None

    # Permissions
    permission_required = "events.add_event"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("cosmos_events:events-list")


class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    template_name = "events/event_update.html"
    form_class = EventForm
    success_url = None

    # Permissions
    permission_required = "events.change_event"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("cosmos_events:events-list")


class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("cosmos_events:events-list")

    # Permissions
    permission_required = "events.delete_event"
    raise_exception = True


class EventFeed(ICalFeed):
    """
    A simple event calender
    """

    def __init__(self):
        super().__init__()
        # Handle exception thrown during migrations, as it checks all routes first for some reason, leading
        # to an error, as there will not be any sites yet on an empty database
        try:
            self.domain = Site.objects.get_current().domain
        except:  # noqa
            self.domain = ""
        self.product_id = "-//" + self.domain + "//Events//EN"
        self.timezone = "Europe/Amsterdam"
        self.file_name = "event.ics"

    def items(self):
        return Event.objects.all().order_by("-start_date_time").filter(end_date_time__gte=datetime.datetime.today())

    def item_guid(self, item):
        return "{}{}".format(item.pk, "global_name")

    def item_title(self, item):
        return "{}".format(item.name)

    def item_description(self, item):
        return item.lead

    def item_start_datetime(self, item):
        return item.start_date_time

    def item_end_datetime(self, item):
        return item.end_date_time

    def item_link(self, item):
        return item.get_absolute_url()
