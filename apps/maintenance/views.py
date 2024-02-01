from rest_framework.generics import CreateAPIView

from .serializers import MaintenanceBookingSerializer


class MaintenanceBookingCreateView(CreateAPIView):
    serializer_class = MaintenanceBookingSerializer

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
