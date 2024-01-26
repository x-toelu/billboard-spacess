from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .models import Billboard
from .serializers import BillBoardCreationSerializer, BillboardDetailSerializer, BillboardListSerializer


class BillboardListView(ListAPIView):
    queryset = Billboard.objects.all()
    serializer_class = BillboardListSerializer

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


class BillboardDetailView(RetrieveAPIView):
    queryset = Billboard.objects.all()
    serializer_class = BillboardDetailSerializer


class BillboardListByCategoryAPIView(ListAPIView):
    serializer_class = BillboardListSerializer

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Billboard.objects.filter(size=category)
