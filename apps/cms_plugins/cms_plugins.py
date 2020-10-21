from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    BoardListPluginModel,
    BoardSubpageTitlePluginModel,
    CommitteeListPluginModel,
    CommitteeSubpageTitlePluginModel,
    TextImagePluginModel,
)

MODULE_NAME = "Cosmos"


# Here the django cms plugins are defined and registered.
# (Almost) every plugin will need a model associated with it to store the information needed
# The render template is the html file that this plugin uses
# Currently no caching is used on the website so it is disabled (enabled by default)
# Caching cannot be applied to plugins that are dynamic on the current user or other dynamic properties of the request
# http://docs.django-cms.org/en/latest/how_to/custom_plugins.html
# http://docs.django-cms.org/en/latest/how_to/caching.html


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
