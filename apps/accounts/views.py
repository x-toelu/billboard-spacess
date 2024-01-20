from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import Response, status

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
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
    permission_classes = [IsOwnerOrReadOnly]
    allowed_methods = ['PUT']

    def patch(self, request, *args, **kwargs):
        error_data = {
            "errors": ["Method 'PATCH' not allowed."],
            "message": "MethodNotAllowed",
        }
        return Response(error_data, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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


class PasswordResetConfirmView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = serializer.validated_data.get('uid')
        token = serializer.validated_data.get('token')
        password = serializer.validated_data.get('password')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None

        # change password if token is valid and not expired.
        if user and default_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'detail': 'Password reset successful.'})
        else:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
