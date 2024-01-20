from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import Response, status

from .serializers import (
    PasswordResetRequestSerializer,
    UpdateProfileSerializer,
    UserSerializer,
)


class UserCreationView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateProfileView(UpdateAPIView):
    """
    Updates part of user profile with PUT request.
    """
    serializer_class = UpdateProfileSerializer
    queryset = get_user_model().objects.all()
    allowed_methods = ['PUT']

    def patch(self, request, *args, **kwargs):
        error_data = {
            "errors": ["Method 'PATCH' not allowed."],
            "message": "MethodNotAllowed",
        }
        return Response(error_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class PasswordResetRequestView(CreateAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = get_user_model().objects.filter(email=email).first()
        if user:
            # Generate token and send reset email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f'{settings.FRONTEND_RESET_URL}/{uid}/{token}/'

            # Send email with reset link
            send_mail(
                'Password Reset',
                f'Click the following link to reset your password: {reset_link}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

        return Response({'detail': 'Password reset email sent.'})
