from django.urls import path

from .views import BillBoardBookingCreateView, VerifyPaymentView

urlpatterns = [
    path(
        'pay/<int:billboard_id>/',
        BillBoardBookingCreateView.as_view(),
        name='create-booking'
    ),
    path(
        'verify/<int:booking_id>/',
        VerifyPaymentView.as_view(),
        name='verify-booking'
    ),
]
