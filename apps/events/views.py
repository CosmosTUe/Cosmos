from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.events.forms import EventForm
from apps.events.models import Event
from cosmos.settings import LOGIN_URL


def events_list(request):
    if not request.user.is_authenticated:
        events_list = Event.objects.filter(member_only=False).order_by("-start_time")
    else:
        events_list = Event.objects.order_by("-start_time").all()
    context = {
        "events_list": events_list,
    }
    return render(request, "events/events_list.html", context)


def event_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {"event": event}
    if event.member_only and not request.user.is_authenticated:
        return redirect("%s?next=%s" % (LOGIN_URL, request.path))
    return render(request, "events/event_view.html", context)


class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Event
    template_name = "events/event_create.html"
    form_class = EventForm
    success_url = None

    # Permissions
    permission_required = "cosmos.add_event"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("events-list")


class EventUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Event
    template_name = "events/event_update.html"
    form_class = EventForm
    success_url = None

    # Permissions
    permission_required = "cosmos.change_event"
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("events-list")


class EventDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("events-list")

    # Permissions
    permission_required = "cosmos.delete_event"
    raise_exception = True
