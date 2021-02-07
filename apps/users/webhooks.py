import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt


# TODO consider changing to /hook/sendgrid?
# link is at `<domain>/accounts/hook/`
# test with `ngrok http <django_port=8000>`
# fully setup with live server:
# https://sendgrid.com/docs/for-developers/tracking-events/getting-started-event-webhook/


@csrf_exempt
def sendgrid_webhook(request: WSGIRequest):
    if request.method != "POST":
        return

    data = json.loads(request.body)
    filtered_data = filter(lambda x: x["event"] == "unsubscribe", data)
    for thing in filtered_data:
        print(thing)
    # print(json.loads(request.body))
    return HttpResponse()
