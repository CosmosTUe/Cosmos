from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.urls import reverse

from .forms import ContactForm
from .models import (
    BoardListPluginModel,
    CommitteeListPluginModel,
    ContactPluginModel,
    TextImagePluginModel,
    CommitteeSubpageTitlePluginModel,
    BoardSubpageTitlePluginModel,
)

MODULE_NAME = "Cosmos"


@plugin_pool.register_plugin
class CommitteeListPluginPublisher(CMSPluginBase):
    model = CommitteeListPluginModel
    render_template = "cms/committee_list.html"
    cache = False
    module = MODULE_NAME
    name = "Committee List"


@plugin_pool.register_plugin
class BoardListPluginPublisher(CMSPluginBase):
    model = BoardListPluginModel
    render_template = "cms/board_list.html"
    cache = False
    module = MODULE_NAME
    name = "Board List"


@plugin_pool.register_plugin
class CommitteeSubpageTitlePluginPublisher(CMSPluginBase):
    model = CommitteeSubpageTitlePluginModel
    render_template = "cms/committee_subpage_title.html"
    cache = False
    module = MODULE_NAME
    name = "Committee Subpage Title"


@plugin_pool.register_plugin
class BoardSubpageTitlePluginPublisher(CMSPluginBase):
    model = BoardSubpageTitlePluginModel
    render_template = "cms/board_subpage_title.html"
    cache = False
    module = MODULE_NAME
    name = "Board Subpage Title"


@plugin_pool.register_plugin
class TextImagePluginPublisher(CMSPluginBase):
    model = TextImagePluginModel
    render_template = "cms/image_text_card.html"
    cache = False
    module = MODULE_NAME
    name = "Text and Image Card"

    def render(self, context, instance, placeholder):
        context.update(
            {"title": instance.committee.name, "subtitle": instance.subtitle, "description": instance.description}
        )
        return context


@plugin_pool.register_plugin
class ContactPlugin(CMSPluginBase):
    model = ContactPluginModel
    name = "Contact"
    render_template = "cms/contacts/contact.html"
    # Groups the plugin inside of "COSMOS"
    module = MODULE_NAME

    def render(self, context, instance, placeholder):
        # Get request.path instead of the referer since this form will appear alongside real content,
        # unlike a contact form page, which is standalone
        request = context.get("request")
        path = "" if request is None else request.path

        form = ContactForm(initial={"referer": path})
        context.update({"title": instance.title, "form": form, "form_action": reverse("ajax_contact")})
        return context
