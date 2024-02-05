from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from .models import Billboard
from .serializers import BillBoardCreationSerializer, BillboardDetailSerializer, BillboardListSerializer


class BillboardListView(ListAPIView):
    serializer_class = BillboardListSerializer

    def get_queryset(self):
        queryset = Billboard.objects.filter(is_booked=False, is_verified=True)
        state = self.request.query_params.get('state')
        size = self.request.query_params.get('size')

        if state:
            queryset = queryset.filter(state=state)
        if size:
            queryset = queryset.filter(size=size)

        return queryset


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
    queryset = Billboard.objects.filter(is_verified=True)
    serializer_class = BillboardDetailSerializer


class NewlyAddedBillboardListView(BillboardListView):
    pagination_class = None

    def get_queryset(self):
        return self.get_queryset()[:5]


class BillboardListByCategoryAPIView(BillboardListView):
    pagination_class = None

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Billboard.objects.filter(size=category, is_verified=True)


class BillboardUserListView(BillboardListView):
    pagination_class = None

    def get_queryset(self):
        return Billboard.objects.filter(is_booked=False, owner=self.request.user)
