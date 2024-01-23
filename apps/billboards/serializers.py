from rest_framework import serializers

from .models import Billboard
from dateutil.relativedelta import relativedelta


class BillboardSerializer(serializers.ModelSerializer):
    available_date_in_days = serializers.SerializerMethodField()
    available_date_in_weeks = serializers.SerializerMethodField()
    available_date_in_months = serializers.SerializerMethodField()

    class Meta:
        model = Billboard
        fields = [
            'owner',
            'image',
            'size',
            'location',
            'available_date',
            'available_date_in_days',
            'available_date_in_weeks',
            'available_date_in_months',
            'target_audience',
            'created_at',
        ]

    def get_available_date_in_days(self, obj):
        print(obj.image, 'kool')
        days = (obj.available_date_to - obj.available_date_from).days + 1
        return  f"{days} days"

    def get_available_date_in_weeks(self, obj):
        weeks = (obj.available_date_to - obj.available_date_from).days // 7
        return  f"{weeks} weeks"

    def get_available_date_in_months(self, obj):
        months = relativedelta(obj.available_date_to, obj.available_date_from).months
        return  f"{months} months"

