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
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=400)
    Button = models.BooleanField(default=False, verbose_name="use button")
    ButtonLink = models.URLField(blank=True)
    ButtonText = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to="cardImg", default="img/default.jpg")
    orientation = models.BooleanField(default=False, verbose_name="image on the left")

    def __str__(self):
        return "TextImageCard:" + self.title
