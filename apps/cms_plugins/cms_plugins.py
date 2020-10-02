# This file is used to create new plugins for the CMS

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import (
    BoardListPluginModel,
    BoardSubpageTitlePluginModel,
    CommitteeListPluginModel,
    CommitteeSubpageTitlePluginModel,
    TextImagePluginModel,
)

# name used to group custom plugins in plugin picker
MODULE_NAME = "Cosmos"


# register_plugin is necessary for django cms to use the created plugin
@plugin_pool.register_plugin
class CommitteeListPluginPublisher(CMSPluginBase):
    # defines the model used for the plugin
    model = CommitteeListPluginModel
    # defines the template used by the plugin
    render_template = "cms/committee_list.html"
    # define if whether the plugin is cachable
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
