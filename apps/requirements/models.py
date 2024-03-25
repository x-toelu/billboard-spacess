from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.accounts.choices import State


class BillboardRequirement(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='billboard_requirements',
        on_delete=models.SET_NULL,
        null=True
    )
    state = models.CharField(max_length=255, choices=State.choices)
    link = models.URLField(max_length=255, blank=True, null=True)
    document = CloudinaryField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.link and not self.document:
            raise ValidationError(
                "Either a link or a document must be provided."
            )
        super().save(*args, **kwargs)
