import logging
import os
from smtplib import SMTPAuthenticationError, SMTPSenderRefused

from cms.models.pagemodel import Page
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import FormView

from apps.cms_plugins.forms import CONTACTS, ContactForm
from cosmos import settings

logger = logging.getLogger(__name__)


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = os.path.join("plugins", "contacts", "contact.html")

    def get_initial(self):
        """
        Record where the visitor was BEFORE arriving at the contact page.
        """
        initial = super().get_initial()
        initial["referer"] = (self.request.GET.get("HTTP_REFERER", ""),)
        return initial

    def get_success_url(self):
        # Redirect user when form is success
        page = get_object_or_404(Page, reverse_id="contact_form_submission", publisher_is_draft=False)
        return page.get_absolute_url()

    def form_valid(self, form):
        """
        Sends the email if the form is valid
        """
        data = form.cleaned_data
        # Add title of board onto data
        data["board"] = CONTACTS.get(data["recipient"])
        # TODO change to your own email for testing purposes
        # data["recipient"] = "testing@email.pp"

        # Create contact email to board member
        board_email_subject = render_to_string(
            os.path.join("plugins", "contacts", "board-email-subject.txt"), {"data": data}
        )
        board_email_body = render_to_string(os.path.join("plugins", "contacts", "board-email-body.txt"), {"data": data})

        # Create confirmation email to sender
        confirm_email_subject = render_to_string(
            os.path.join("plugins", "contacts", "confirm-email-subject.txt"), {"data": data}
        )
        confirm_email_body = render_to_string(
            os.path.join("plugins", "contacts", "confirm-email-body.txt"), {"data": data}
        )
        try:
            # TODO consider sending the same email to sender and recipient, one as bcc?
            logger.info("Sending to board...")
            # Send contact email to board member
            send_mail(
                board_email_subject,
                board_email_body,
                settings.EMAIL_HOST_USER,
                [data["recipient"]],
                fail_silently=(not settings.DEBUG),
            )

            # Send confirmation email to sender
            logger.info("Sending confirmation to sender...")
            send_mail(
                confirm_email_subject,
                confirm_email_body,
                settings.EMAIL_HOST_USER,
                [data["from_email"]],
                fail_silently=(not settings.DEBUG),
            )
        except (SMTPAuthenticationError, SMTPSenderRefused):
            if settings.DEBUG:
                raise
            # TODO inform usere that email is not configured correctly
            # form.add_error(django.forms.forms.NON_FIELD_ERRORS, "Email is not configured on the server side")
            # return JsonResponse(form.errors, status=501)

        logger.info("Emails sent!")
        return super().form_valid(form)


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)

    Source: https://docs.djangoproject.com/en/3.0/topics/class-based-views/generic-editing/#ajax-example
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {"msg": "Success!"}
            return JsonResponse(data)
        else:
            return response


class ContactFormAjaxView(AjaxableResponseMixin, ContactFormView):
    # CMSPlugin's render() method handles the initial GET request/response and creation of the initial form object
    # We only need to care about POST requests
    http_method_names = ["post"]

    def get_success_url(self):
        # Return the user to the same page when the form is a success
        return self.request.path
