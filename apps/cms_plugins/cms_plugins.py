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
