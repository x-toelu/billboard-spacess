from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import UpdateProfileView, UserCreationView

urlpatterns = [
    path('create/', UserCreationView.as_view(), name='users_create'),
    path('update-profile/<str:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
