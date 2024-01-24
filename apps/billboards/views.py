from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Billboard
from .serializers import BillboardSerializer, BillBoardCreationSerializer


class BillboardListView(ListAPIView):
    queryset = Billboard.objects.all()
    serializer_class = BillboardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(booked=False)


class BillboardCreateView(CreateAPIView):
    queryset = Billboard.objects.all()
    serializer_class = BillBoardCreationSerializer

    def perform_create(self, serializer):
        """
        Create a billboard with current user as the owner.
        """
        user = self.request.user
        return serializer.save(owner=user)
