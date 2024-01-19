from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlencode
from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import Response, status

from .serializers import InputSerializer, UpdateProfileSerializer, UserSerializer


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


def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


class GoogleLoginApi(GenericAPIView):
    serializer_class = InputSerializer

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_FRONTEND_URL}/google/'
        access_token = google_get_access_token(code=code,
                                               redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = get_user_model().objects.get(email=user_data['email'])
            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)
        except get_user_model().DoesNotExist:
            full_name = user_data.get('given_name', '') + user_data.get('family_name', '')

            user = get_user_model().objects.create(
                email=user_data['email'],
                full_name=full_name,
            )

            access_token, refresh_token = generate_tokens_for_user(user)
            response_data = {
                'user': UserSerializer(user).data,
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return Response(response_data)
