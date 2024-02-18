from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

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

    # paystack subscription requirements
    paystack_sub_code = models.CharField(max_length=100, null=True)
    paystack_email_token = models.CharField(max_length=100, null=True)

    is_active = models.BooleanField(default=True)

    @property
    def has_expired(self):
        """
        Checks if the subscription has expired.
        """
        return self.expires_at is not None and self.expires_at <= timezone.localtime()

    def renew_subscription(self, duration):
        """
        Renews the subscription for the given duration.
        """
        new_expiration = self._calculate_new_expiration(duration)
        self.expires_at = new_expiration
        self.save()

    def _calculate_new_expiration(self, duration):
        """
        Calculate new expiration date based
        on current expiration date and given duration.
        """
        if self.expires_at:
            return self.expires_at + timedelta(days=duration)
        else:
            return timezone.localtime() + timedelta(days=duration)

    def __str__(self):
        return f"{self.user}'s subscription ({self.plan})"
