from rest_framework import serializers

from apps.accounts.serializers import MiniUserSerializer
from apps.subscriptions.validators import SubscriptionValidator

from .models import Billboard


class BillBoardCreationSerializer(SubscriptionValidator, serializers.ModelSerializer):
    owner = MiniUserSerializer(read_only=True)
    image = serializers.FileField(required=True)

    class Meta:
        model = Billboard
        fields = [
            'owner',
            'image',
            'size',
            'location',
            'price',
            'state',
            'target_audience',
        ]

    def validate(self, data):
        user = self.context['request'].user
        self.validate_create_billboards(user)
        return data


class BillboardListSerializer(serializers.ModelSerializer):
    owner = MiniUserSerializer(read_only=True)
    location = serializers.CharField(source='full_location')
    image = serializers.SerializerMethodField()

    class Meta:
        model = Billboard
        fields = [
            'id',
            'owner',
            'size',
            'image',
            'location',
        ]

    def get_image(self, document):
        """Returns full image url"""
        request = self.context.get('request')
        file_url = document.image.url
        return request.build_absolute_uri(file_url)


class BillboardDetailSerializer(BillboardListSerializer):
    class Meta:
        model = Billboard
        fields = BillboardListSerializer.Meta.fields + [
            'is_booked',
            'target_audience',
            'created_at',
        ]
