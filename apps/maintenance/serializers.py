from rest_framework import serializers

from apps.accounts.serializers import MiniUserSerializer

from .models import MaintenanceBooking


class MaintenanceBookingSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = MaintenanceBooking
        fields = [
            'user',
            'email',
            'phone_number',
            'location',
            'description',
            'preferred_date',
            'preferred_time',
        ]
