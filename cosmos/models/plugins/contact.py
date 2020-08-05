from cms.models import CMSPlugin
from django.db import models


class ContactPluginModel(CMSPlugin):
    title = models.CharField("title", blank=True, help_text="Optional. Title of the widget.", max_length=64,)
