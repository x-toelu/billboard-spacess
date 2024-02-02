from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView

from apps.billboards.models import Billboard

from .serializers import BillboardBookingSerializer


class BillBoardBookingCreateView(CreateAPIView):
    serializer_class = BillboardBookingSerializer

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
