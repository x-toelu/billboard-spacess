from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer to request for a password change
    """
    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for reseting user's password
    """
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True)
