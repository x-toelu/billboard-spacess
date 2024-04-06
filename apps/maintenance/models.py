from django.contrib.auth import get_user_model
from django.db import models


class MaintenanceBooking(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='maintenance_bookings',
        on_delete=models.CASCADE
    )
    location = models.CharField(max_length=255)
    description = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    is_fixed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
