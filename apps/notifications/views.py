from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView

from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailAPIView(RetrieveAPIView):
    """
    Mark a single notification as read.
    """
    serializer_class = NotificationSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkAllNotificationsAsReadAPIView(GenericAPIView):
    """
    Marks all notifications as read.
    """
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        notifications = Notification.objects.filter(user=user, is_read=False)

        for notif in notifications:
            notif.mark_as_read()

        return Response({"message": "All notifications marked as read"})

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
