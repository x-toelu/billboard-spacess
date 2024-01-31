from django.contrib.auth import get_user_model
from django.db import models

from utils.constants import NIGERIAN_STATES


class Maintenance(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='maintenance_bookings',
        on_delete=models.CASCADE
    )
    location = models.CharField(max_length=255)
    state = models.CharField(max_length=255, choices=NIGERIAN_STATES)
    description = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)
