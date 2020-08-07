from django.db import models
from cms.plugin_base import CMSPlugin

from cosmos.models import Committee, Board


class CommitteeListPluginModel(CMSPlugin):
    committees = models.ManyToManyField(Committee)

    def __str__(self):
        return "test"


class BoardListPluginModel(CMSPlugin):
    boards = models.ManyToManyField(Board)

    def __str__(self):
        return "test"
