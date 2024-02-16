from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    GoogleSignInView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    UpdateProfileView,
    UserCreationView,
    UserDetailView,
)

urlpatterns = [
    path('create/', UserCreationView.as_view(), name='users_create'),
    path('users/<str:pk>/', UserDetailView.as_view(), name='users_detail'),
    path(
        'update-profile/<str:pk>/',
        UpdateProfileView.as_view(),
        name='update_profile'
    ),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path(
        'password/reset/',
        PasswordResetRequestView.as_view(),
        name='password-reset-request'
    ),
    path(
        'password/reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'
    ),

    path("google-signup/", GoogleSignInView.as_view(), name='google-signup')
]
