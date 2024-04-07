from django.urls import path

from .views import SubscriptionView, VerifySubscriptionView

urlpatterns = [
    path('', SubscriptionView.as_view(), name='create-subscription'),
    path('verify/<str:sub_id>/', VerifySubscriptionView.as_view(), name='verify-sub'),
]
