from decimal import Decimal

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from utils.constants import NIGERIAN_STATES


class Billboard(models.Model):
    SIZE_CHOICES = (
        ('potrait', 'Potrait'),
        ('large_format', 'Large Format'),
        ('48_sheet', '48 Sheet'),
        ('spectacular_billboard', 'Spectacular Billboard'),
        ('gantry', 'Gantry'),
        ('unipole', 'Unipole'),
    )

    owner = models.ForeignKey(
        get_user_model(),
        related_name='billboards',
        on_delete=models.CASCADE
    )
    image = CloudinaryField()
    size = models.CharField(max_length=21, choices=SIZE_CHOICES)
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=NIGERIAN_STATES)
    target_audience = models.CharField(max_length=255)

    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=Decimal('0.00')
    )

    is_booked = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified_at = models.DateTimeField(blank=True, null=True)

    @property
    def full_location(self):
        return f"{self.location}, {self.state.capitalize()} State."

    def save(self, *args, **kwargs):
        if self.is_verified and not self.is_verified_at:
            self.is_verified_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_verified_at']

    def __str__(self) -> str:
        return f"{self.owner.display_name}'s billboard at {self.location}"
