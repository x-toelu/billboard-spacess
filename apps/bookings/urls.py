from django.urls import path

from .views import BillBoardBookingCreateView

urlpatterns = [
    path('', BillBoardBookingCreateView.as_view(), name='billboards-list'),
]
