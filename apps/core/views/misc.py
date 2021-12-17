import os

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django_sendfile import sendfile

import secret_settings
from cosmos.settings import SENDFILE_ROOT


def protected_media(request, file_path):
    user = request.user

    if file_path.startswith("gmm/") and not user.is_authenticated:
        raise PermissionDenied()

    return sendfile(request, SENDFILE_ROOT + file_path)


def update_door_status(request):
    global door_status
    try:
        request_token = request.GET.get("access_token")
        status = int(request.GET.get("status"))
        pi_token = secret_settings.secrets["TOKENS"]["CR-DOOR"]

        if request_token == pi_token:
            if status == 1:
                f = open("/tmp/door-open", "w")
                f.close()
            elif status == 0:
                if os.path.exists("/tmp/door-open"):
                    os.remove("/tmp/door-open")

            return HttpResponse("Updated door status")
        return HttpResponse("Invalid token", status=401)
    except Exception:
        return HttpResponse("There was an error updating the door status", status=400)
