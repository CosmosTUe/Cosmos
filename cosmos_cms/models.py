from cms.plugin_base import CMSPlugin
from django.db import models

from cosmos.models import Board, Committee


class CommitteeListPluginModel(CMSPlugin):
    committees = models.ManyToManyField(Committee)

    def copy_relations(self, oldinstance):
        self.committees.set(oldinstance.committees.all())

    def __str__(self):
        return "CommitteeList:".join(committee.name for committee in self.committees.all())


class BoardListPluginModel(CMSPlugin):
    boards = models.ManyToManyField(Board)

    def copy_relations(self, oldinstance):
        self.boards.set(oldinstance.boards.all())

    def __str__(self):
        return "BoardList:".join(board.name for board in self.boards.all())


class TextImagePluginModel(CMSPlugin):
    title = models.CharField()
    text = models.CharField()
    buttonLink = models.URLField()
    buttonText = models.CharField(max_length=20)
    image = models.ImageField(uploadt_to="cardImg", default="cardImg/default.jpg")
    orientation = models.BooleanField(default=0)

    def __str__(self):
        return "TextImageCard:".join(self.title)
