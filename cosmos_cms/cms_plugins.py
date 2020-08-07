from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import CommitteeListPluginModel, BoardListPluginModel


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
