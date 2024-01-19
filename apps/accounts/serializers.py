from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'password',
            'password2'
        ]

    def validate(self, attrs):
        """
        Validate the password and password2 fields to ensure they match.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return get_user_model().objects.create_user(**validated_data)


class UpdateProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    display_name = serializers.CharField(required=True)
    user_field = serializers.ChoiceField(
        required=True,
        choices=get_user_model().USER_CHOICES
    )
    state_of_residence = serializers.ChoiceField(
        required=True,
        choices=get_user_model().NIGERIAN_STATES
    )

    class Meta:
        model = get_user_model()
        fields = [
            'user_field',
            'full_name',
            'phone_number',
            'state_of_residence',
            'display_name'
        ]


class InputSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)
