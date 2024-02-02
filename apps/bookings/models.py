from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from apps.billboards.models import Billboard
from utils.constants import MONTHS_IN_YEAR, WEEKS_IN_MONTH


class Booking(models.Model):
    BOOKING_PERIOD = (
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
        ('annually', 'annually'),
    )

    user = models.ForeignKey(
        get_user_model(),
        related_name="bookings",
        on_delete=models.CASCADE
    )
    billboard = models.ForeignKey(
        Billboard,
        related_name="bookings",
        on_delete=models.CASCADE
    )
    period = models.CharField(max_length=8, choices=BOOKING_PERIOD)
    timeline = models.PositiveSmallIntegerField()

    paid = models.BooleanField(default=False)
    paystack_ref = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __get_price(self):
        period_multiplier = {
            'weekly': 1 / WEEKS_IN_MONTH,
            'monthly': 1,
            'annually': MONTHS_IN_YEAR,
        }

        if self.period in period_multiplier:
            return self.billboard.price * Decimal(period_multiplier[self.period])
        else:
            raise ValueError('Invalid booking period')

    @property
    def amount(self):
        return self.timeline * self.__get_price()

    def __str__(self) -> str:
        return f"₦{self.amount} {self.period}({self.timeline}) booking for billboard @ {self.billboard.full_location}"
