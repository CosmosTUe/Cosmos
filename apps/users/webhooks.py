import json

from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseForbidden

from oauth2_provider.views.generic import ProtectedResourceView
from sendgrid import EventWebhookHeader

from sendgrid.helpers.eventwebhook import EventWebhook

from cosmos import settings

webhook = EventWebhook()

# TODO consider changing to /hook/sendgrid?
# link is at `<domain>/accounts/hook/`
# test with `ngrok http 127.0.0.1:<django_port=8000>`
# fully setup with live server:
# https://sendgrid.com/docs/for-developers/tracking-events/getting-started-event-webhook/
# create token
# https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#client-credential


def is_valid_signature(request: WSGIRequest) -> bool:
    """
    Determines whether the request has a valid signature

    https://github.com/sendgrid/sendgrid-python/blob/3f97a7fed7b48d7cbe3b80db81abf5bb170bf102/examples/helpers/eventwebhook/eventwebhook_example.py#L6

    :param request: Django request
    :returns: boolean
    """
    return webhook.verify_signature(
        request.body.decode("utf-8"),
        request.headers[EventWebhookHeader.SIGNATURE],
        request.headers[EventWebhookHeader.TIMESTAMP],
        webhook.convert_public_key_to_ecdsa(settings.SENDGRID_WEBHOOK_SIGNATURE),
    )


class SendGridWebhook(ProtectedResourceView):
    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        # TODO must be tested on live server (integration testing doesn't set signatures)
        if not is_valid_signature(request):
            return HttpResponseForbidden()

        data = json.loads(request.body.decode("utf-8"))
        filtered_data = filter(lambda x: x["event"] == "unsubscribe", data)
        for thing in filtered_data:
            # search amongst institution emails
            query = User.objects.filter(username=thing["email"])

            # if there are no institution emails found
            # NOTE: institution emails are primary keys therefore cannot have duplicates
            if len(query) != 1:
                query = User.objects.filter(email=thing["email"])

                # if there are no alt emails found, skip unsubscribing
                # TODO or if there are more than than one alt emails found,
                #  indicate multiple users sharing the same account?
                if len(query) != 1:
                    continue

            user = query.first()
            user.profile.subscribed_newsletter = False
            user.profile.save()

        return HttpResponse()
