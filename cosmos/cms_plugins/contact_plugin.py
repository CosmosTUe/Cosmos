import os

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.urls import reverse

from cosmos.forms.contact import ContactForm
from cosmos.models.plugins.contact import ContactPluginModel


@plugin_pool.register_plugin
class ContactPlugin(CMSPluginBase):
    model = ContactPluginModel
    name = "Contact"
    render_template = os.path.join("plugins", "contacts", "contact.html")
    # Groups the plugin inside of "COSMOS"
    module = "COSMOS"

    def render(self, context, instance, placeholder):
        # Get request.path instead of the referer since this form will appear alongside real content,
        # unlike a contact form page, which is standalone
        request = context.get("request")
        path = "" if request is None else request.path

        form = ContactForm(initial={"referer": path})
        context.update({"title": instance.title, "form": form, "form_action": reverse("ajax_contact")})
        return context
