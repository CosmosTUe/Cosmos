from django.urls import path

import apps.events.views

app_name = "cosmos_events"

urlpatterns = [
    path("add/", apps.events.views.EventCreate.as_view(), name="events-create"),
    path("list/", apps.events.views.events_list, name="events-list"),
    path("archive/", apps.events.views.events_archive, name="events-archive"),
    path("feed/", apps.events.views.EventFeed(), name="events-feed"),
    path("<int:pk>/", apps.events.views.event_view, name="events-view"),
    path("<int:pk>/update/", apps.events.views.EventUpdate.as_view(), name="events-update"),
    path("<int:pk>/delete/", apps.events.views.EventDelete.as_view(), name="events-delete"),
]
