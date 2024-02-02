from django.urls import path

from .views import BillBoardBookingCreateView

urlpatterns = [
    path('<int:billboard_id>/', BillBoardBookingCreateView.as_view(), name='billboards-list'),
]
