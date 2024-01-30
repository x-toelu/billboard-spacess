from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from utils.constants import NIGERIAN_STATES


class BillboardRequirement(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='billboard_requirements',
        on_delete=models.SET_NULL,
        null=True
    )
    state = models.CharField(max_length=255, choices=NIGERIAN_STATES)
    link = models.URLField(max_length=255, null=True)
    document = models.FileField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.link and not self.document:
            raise ValidationError(
                "Either a link or a document must be provided."
            )
