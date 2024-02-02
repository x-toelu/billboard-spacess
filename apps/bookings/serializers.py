from rest_framework import serializers

from apps.billboards.serializers import BillboardListSerializer

from .models import Booking


class BillboardBookingSerializer(serializers.ModelSerializer):
    billboard = BillboardListSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'billboard',
            'period',
            'timeline',
            'amount',
        ]
