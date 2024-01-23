from rest_framework.generics import ListAPIView

from .models import Billboard
from .serializers import BillboardSerializer


class BillboardListView(ListAPIView):
    queryset = Billboard.objects.all()
    serializer_class = BillboardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(booked=False)
