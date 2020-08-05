import os

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import FormView
from cms.models.pagemodel import Page

from cosmos import settings
from cosmos.cms_plugins.contact_plugin import ContactForm


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = os.path.join("plugins", "contacts", "contact.html")

    def get_initial(self):
        """
        Record where the visitor was BEFORE arriving at the contact page.
        """
        initial = super().get_initial()
        print(self.request)
        print(type(self.request))
        print(type(self.request.GET))
        initial["referer"] = (self.request.GET.get("HTTP_REFERER", ""),)
        return initial

    def get_success_url(self):
        page = get_object_or_404(Page, reverse_id="contact_form_submission", publisher_is_draft=False)
        return page.get_absolute_url()

    def form_valid(self, form):
        """
        TODO Send the email if the form is valid
        """

        email_subject = render_to_string(os.path.join("contacts", "email-subject"), {"contact", self})
        email_body = render_to_string(os.path.join("contacts", "email-body"), {"contact", self})
        print("I am attempting to send!")
        print(f"self={self}")

        FROM_EMAIL = "test@test.test"
        RECIPIENT_LIST = "test@test.test"
        try:
            send_mail(email_subject, email_body, FROM_EMAIL, RECIPIENT_LIST, fail_silently=(not settings.DEBUG))
        except Exception:
            # TODO explore more specific errors
            if settings.DEBUG:
                raise
        return super().form_valid(form)
