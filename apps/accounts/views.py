from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import Response, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import UpdateProfileSerializer, UserSerializer


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
