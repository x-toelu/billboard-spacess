from django.urls import path

from .views import BillBoardBookingCreateView

urlpatterns = [
    path(
        'pay/<int:billboard_id>/',
        BillBoardBookingCreateView.as_view(), name='create-booking'
    ),
]
