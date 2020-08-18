from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import BoardListPluginModel, CommitteeListPluginModel, TextImagePluginModel


@plugin_pool.register_plugin
class CommitteeListPluginPublisher(CMSPluginBase):
    model = CommitteeListPluginModel
    render_template = "cms/committee_list.html"
    cache = False
    module = "Cosmos"
    name = "Committee List"


@plugin_pool.register_plugin
class BoardListPluginPublisher(CMSPluginBase):
    model = BoardListPluginModel
    render_template = "cms/board_list.html"
    cache = False
    module = "Cosmos"
    name = "Board List"


@plugin_pool.register_plugin
class TextImagePluginPublisher(CMSPluginBase):
    model = TextImagePluginModel
    render_template = "cms/image_text_card.html"
    cache = False
    module = ""
    name = "Text and Image Card"
