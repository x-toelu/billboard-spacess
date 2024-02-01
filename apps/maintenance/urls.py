from django.urls import path

from .views import MaintenanceBookingCreateView

urlpatterns = [
    path(
        '',
        MaintenanceBookingCreateView.as_view(),
        name='maintenance-booking-create'
    )
]
