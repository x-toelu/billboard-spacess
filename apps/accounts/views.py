import hashlib
import random
import string

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken

from helpers.password_reset import reset_password_expire_otp
from services.google_auth import GoogleAuth

from .serializers import (
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    UpdateProfileSerializer,
    UserCreationSerializer,
    UserSerializer
)


class UserCreationView(CreateAPIView):
    """
    Allows users to create a new account by providing required user information.
    """
    serializer_class = UserCreationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        return Response({
            **serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class UserDetailView(RetrieveAPIView):
    """
    Returns detailed information about a user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UpdateProfileView(UpdateAPIView):
    """
    Updates user profile.
    """
    serializer_class = UpdateProfileSerializer
    queryset = get_user_model().objects.all()

    def get_object(self):
        user = self.request.user
        queryset = self.filter_queryset(self.get_queryset())
        object = get_object_or_404(queryset, email=user.email)

        return object


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
            self.create_and_send_otp(user, email)
        return Response({'message': 'Password reset email sent.'})

    def create_and_send_otp(self, user, email):
        otp = ''.join(random.choices(string.digits, k=6))
        hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
        user.password_reset_otp = hashed_otp
        user.password_reset_otp_created_at = timezone.now()
        user.save()

        # Send OTP via email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )


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
        hashed_input_otp = hashlib.sha256(otp.encode()).hexdigest()

        if user and user.password_reset_otp == hashed_input_otp:
            success, message = reset_password_expire_otp(user, password)

            if success:
                return Response({'message': message})
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


#  Google Auth


class GoogleSignInView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        redirect_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/userinfo.email&access_type=offline&redirect_uri={settings.GOOGLE_REDIRECT_URI}"

        return redirect(redirect_url)


class GoogleRedirectURIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response({"message: An error occured"}, status.HTTP_400_BAD_REQUEST)

        google_auth = GoogleAuth()
        user_info = google_auth.get_user_info(code)

        if user_info:
            try:
                user = get_user_model().objects.get(email=user_info["email"])
            except get_user_model().DoesNotExist:
                user = get_user_model().objects.create_user(
                    email=user_info["email"],
                    full_name=user_info["name"]
                )

            refresh_token = RefreshToken.for_user(user)
            return Response({
                'id': user.id,
                'email': user.email,
                'access': str(refresh_token.access_token),
                'refresh': str(refresh_token)
            })
