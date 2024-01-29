from rest_framework import serializers

from .models import Billboard
from apps.accounts.serializers import MiniUserSerializer
from dateutil.relativedelta import relativedelta


class BillBoardCreationSerializer(serializers.ModelSerializer):
    owner = MiniUserSerializer(read_only=True)
    image = serializers.ImageField(required=True)

    class Meta:
        model = Billboard
        fields = [
            'owner',
            'image',
            'size',
            'location',
            'state',
            'target_audience',
        ]


class BillboardListSerializer(serializers.ModelSerializer):
    owner = MiniUserSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Billboard
        fields = [
            'id',
            'owner',
            'size',
            'image',
            'full_location',
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
            'booked',
            'target_audience',
            'created_at',
        ]
