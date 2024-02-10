from datetime import datetime, timedelta
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveAPIView,
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import Response, status

from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UpdateProfileSerializer,
    UserCreationSerializer,
    UserSerializer,
)


class UserCreationView(CreateAPIView):
    """
    Allows users to create a new account by providing required user information.
    """
    serializer_class = UserCreationSerializer
    permission_classes = [AllowAny]


class UserDetailView(RetrieveAPIView):
    """
    Returns detailed information about a user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UpdateProfileView(UpdateModelMixin, GenericAPIView):
    """
    Updates part of user profile.
    """
    serializer_class = UpdateProfileSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [AllowAny]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class PasswordResetRequestView(CreateAPIView):
    """
    Initiates password reset requests.

    Allows users to request a password reset by providing their email address.
    If the email corresponds to an existing user, a password reset link is generated,
    and an email containing the link is sent to the user.
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = get_user_model().objects.filter(email=email).first()
        if user:
            otp = ''.join(random.choices(string.digits, k=6))
            user.password_reset_otp = otp
            user.password_reset_otp_created_at = datetime.now()
            user.save()

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

        return Response({'detail': 'Password reset email sent.'})


class PasswordResetConfirmView(CreateAPIView):
    """
    Confirms password reset requests.

    Allow users to confirm password reset requests by providing a valid
    OTP, and a new password.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        password = serializer.validated_data['password']

        user = get_user_model().objects.filter(email=email).first()
        if user and user.password_reset_otp == otp:
            # Check if OTP is expired
            expiration_time = user.password_reset_otp_created_at.replace(tzinfo=None) + timedelta(minutes=15)

            if datetime.now() > expiration_time:
                return Response(
                    {'detail': 'OTP has expired. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # reset password
            user.set_password(password)
            user.save()

            # mark OTP as expired
            user.password_reset_otp = None
            user.password_reset_otp_created_at = None
            user.save()

            return Response({'message': 'Password reset successful.'})
        else:
            return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
