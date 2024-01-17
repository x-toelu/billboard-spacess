from django.urls import path

from .views import UserCreationView

urlpatterns = [
    path('', UserCreationView.as_view(), name='register'),
]
