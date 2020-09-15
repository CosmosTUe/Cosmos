from django.urls import path

from . import views

app_name = "cosmos_legacy"

urlpatterns = [
    path("accounts/import/<uidb64>/<token>/", views.import_user, name="import_user"),
]
