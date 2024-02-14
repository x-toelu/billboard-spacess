from rest_framework import serializers

from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Subscription
        fields = [
            'user',
            'plan',
        ]
