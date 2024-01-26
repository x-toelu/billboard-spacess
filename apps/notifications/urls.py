from django.urls import path

from .views import MarkAllNotificationsAsReadAPIView, NotificationDetailAPIView, NotificationListAPIView

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notification-list'),
    path(
        'read/<int:pk>/',
        NotificationDetailAPIView.as_view(),
        name='notification-detail'
    ),
    path(
        'read/all/',
        MarkAllNotificationsAsReadAPIView.as_view(),
        name='mark-all-notifs-read'
    ),
]
