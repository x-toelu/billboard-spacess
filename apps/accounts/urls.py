from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserCreationView

urlpatterns = [
    path('create/', UserCreationView.as_view(), name='create-user'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
]
