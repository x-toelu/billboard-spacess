from django.contrib.auth import get_user_model
from django.db import models

from .choices import SubscriptionType


class Subscription(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='subscription',
        on_delete=models.CASCADE
    )
    plan = models.CharField(
        max_length=20,
        choices=SubscriptionType.choices,
        default=SubscriptionType.FREE
    )
    expires_at = models.DateTimeField(null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}'s subscription ({self.plan})"
