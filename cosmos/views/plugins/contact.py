import os

# from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# from django.template.loader import render_to_string
from django.views.generic import FormView
from cms.models.pagemodel import Page

# from cosmos import settings
from cosmos.cms_plugins.contact_plugin import ContactForm


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
        TODO Send the email if the form is valid
        """

        # email_subject = render_to_string(
        #     os.path.join("plugins", "contacts", "contact-email-subject.txt"),
        #     {field: form.cleaned_data.get(field) for field in ["name", "subject"]},
        # )
        # email_body = render_to_string(
        #     os.path.join("plugins", "contacts", "contact-email-body.txt"),
        #     {
        #         field: form.cleaned_data.get(field)
        #         for field in ["board", "from_name", "from_email", "telephone", "message"]
        #     },
        # )
        #
        # FROM_EMAIL = "test@test.test"
        # RECIPIENT_LIST = "test@test.test"
        # try:
        #     print("I am attempting to send!")
        #     # send_mail(email_subject, email_body, FROM_EMAIL, RECIPIENT_LIST, fail_silently=(not settings.DEBUG))
        # except Exception:
        #     # TODO explore more specific errors
        #     if settings.DEBUG:
        #         raise
        # confirm_email_subject = render_to_string(
        #     os.path.join("plugins", "contacts", "confirm-email-subject.txt"),
        #     {field: form.cleaned_data.get(field) for field in ["name", "subject"]},
        # )
        # confirm_email_body = render_to_string(
        #     os.path.join("plugins", "contacts", "confirm-email-body.txt"),
        #     {field: form.cleaned_data.get(field) for field in ["from_name", "recipient", "message"]},
        # )
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
