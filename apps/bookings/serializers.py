from rest_framework import serializers

from apps.billboards.serializers import BillboardListSerializer

from .models import Booking


class BillboardBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        read_only_fields = ['billboard']
        fields = [
            'billboard',
            'period',
            'timeline',
            'amount',
        ]
