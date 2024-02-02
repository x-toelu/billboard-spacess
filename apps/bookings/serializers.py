from rest_framework import serializers

from .models import Booking
from apps.accounts.serializers import MiniUserSerializer


class BillboardBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = [
            'billboard',
            'period',
            'timeline',
            'amount',
        ]
