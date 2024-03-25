from rest_framework import serializers

from apps.accounts.serializers import MiniUserSerializer

from .models import BillboardRequirement


class BillboardRequirementSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = BillboardRequirement
        fields = '__all__'
