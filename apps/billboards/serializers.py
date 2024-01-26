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
            'available_date_from',
            'available_date_to',
            'target_audience_from',
            'target_audience_to',
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
            'location',
        ]
    
    def get_image(self, document):
        """Returns full image url"""
        request = self.context.get('request')
        file_url = document.image.url
        return request.build_absolute_uri(file_url)


class BillboardDetailSerializer(BillboardListSerializer):
    available_date_in_days = serializers.SerializerMethodField()
    available_date_in_weeks = serializers.SerializerMethodField()
    available_date_in_months = serializers.SerializerMethodField()

    class Meta:
        model = Billboard
        fields = BillboardListSerializer.Meta.fields + [
            'booked',
            'available_date',
            'available_date_in_days',
            'available_date_in_weeks',
            'available_date_in_months',
            'target_audience',
            'created_at',
        ]

    def get_available_date_in_days(self, obj):
        days = (obj.available_date_to - obj.available_date_from).days + 1
        return f"{days} days"

    def get_available_date_in_weeks(self, obj):
        weeks = (obj.available_date_to - obj.available_date_from).days / 7
        return f"{round(weeks, 1)} weeks"

    def get_available_date_in_months(self, obj):
        months = relativedelta(obj.available_date_to,
                               obj.available_date_from).months
        return f"{months} months"
