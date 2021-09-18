from django.urls import path

import apps.events.views

app_name = "cosmos_users"

urlpatterns = [
    path("add/", apps.events.views.EventCreate.as_view(), name="events-create"),
    path("list/", apps.events.views.events_list, name="events-list"),
    path("<int:pk>/", apps.events.views.event_view, name="events-view"),
    path("<int:pk>/update/", apps.events.views.EventUpdate.as_view(), name="events-update"),
    path("<int:pk>/delete/", apps.events.views.EventDelete.as_view(), name="events-delete"),
]
