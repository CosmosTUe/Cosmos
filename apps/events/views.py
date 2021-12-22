import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_ical.views import ICalFeed

from apps.events.forms import EventForm
from apps.events.models import Event


def events_list(request):
    if request.user.is_authenticated:
        events_list = (
            Event.objects.order_by("start_date_time").filter(end_date_time__gte=datetime.datetime.today()).all()
        )
    else:
        events_list = (
            Event.objects.filter(member_only=False)
            .order_by("start_date_time")
            .filter(end_date_time__gte=datetime.datetime.today())
        )
    context = {
        "events_list": events_list,
    }
    return render(request, "events/events_list.html", context)


def event_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}
    if event.member_only and not request.user.is_authenticated:
        raise PermissionDenied()
    return render(request, "events/event_view.html", context)


def events_archive(request):
    if request.user.is_authenticated:
        events_list = (
            Event.objects.order_by("start_date_time").filter(end_date_time__lt=datetime.datetime.today()).all()
        )
    else:
        events_list = (
            Event.objects.filter(member_only=False)
            .order_by("start_date_time")
            .filter(end_date_time__lt=datetime.datetime.today())
        )
    context = {
        "events_list": events_list,
    }
    return render(request, "events/events_archive.html", context)


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

    domain = Site.objects.get_current().domain
    product_id = "-//" + domain + "//Events//EN"
    timezone = "Europe/Amsterdam"
    file_name = "event.ics"

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
