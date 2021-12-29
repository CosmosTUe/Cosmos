from crum import get_current_user
from django.contrib.auth.models import User
from django.db import models


class InternalDocument(models.Model):
    name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="internal_document_created_by",
    )

    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="internal_document_modified_by",
    )

    file = models.FileField(null=False, blank=False, upload_to="internal/")

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(InternalDocument, self).save(*args, **kwargs)

    def __str__(self):
        return "InternalDocument: {" + self.name + ", " + str(self.date) + "}"
