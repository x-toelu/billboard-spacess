from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .mixins import PasswordValidatorMixin
from .validators import ChoiceFieldsValidator


class UserCreationSerializer(PasswordValidatorMixin, serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'password',
            'password2'
        ]

    def create(self, validated_data):
        validated_data.pop('password2')
        return get_user_model().objects.create_user(**validated_data)


class MiniUserSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='display_name')

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'full_name',
            'business_name',
        ]


class UserSerializer(MiniUserSerializer):
    business_name = serializers.CharField(source='display_name')

    class Meta:
        model = get_user_model()
        fields = MiniUserSerializer.Meta.fields + [
            'phone_number', 'state', 'user_field',
        ]


class UpdateProfileSerializer(ChoiceFieldsValidator, serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    display_name = serializers.CharField(required=True)
    user_field = serializers.CharField(required=True)
    state = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = [
            'user_field',
            'full_name',
            'phone_number',
            'state',
            'display_name'
        ]


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer to request for a password change
    """
    email = serializers.EmailField()


class PasswordResetSerializer(PasswordValidatorMixin, serializers.Serializer):
    """
    Serializer for reseting user's password
    """
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)
