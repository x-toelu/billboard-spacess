from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .choices import State, UserField
from .mixins import PasswordValidatorMixin


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


class UpdateProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    display_name = serializers.CharField(required=True)
    user_field = serializers.CharField(required=True)
    state = serializers.ChoiceField(
        required=True,
        choices=State.choices,
    )

    class Meta:
        model = get_user_model()
        fields = [
            'user_field',
            'full_name',
            'phone_number',
            'state',
            'display_name'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_user_field_choices = set(choice for tuples in UserField.choices for choice in tuples)

    def validate_user_field(self, obj):
        """
        This function manually validates a user field instead of relying on the 
        default `ChoiceField` with the `choices` argument.

        The reason behind this is to address challenges encountered by the 
        frontend dev sending data as required. Because, sometimes we all
        encounter little skill issues & tackling them as a team is part of the fun.
        """

        user_field = obj.lower().split(' ')
        user_field = "-".join(user_field)

        if user_field not in self.valid_user_field_choices:
            raise ValidationError(f'"{obj}" is not a valid choice.')

        return user_field


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
