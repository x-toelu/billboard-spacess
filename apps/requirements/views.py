from rest_framework.generics import ListAPIView

from .models import BillboardRequirement
from .serializers import BillboardRequirementSerializer


class StateBillBoardRequirementListView(ListAPIView):
    pagination_class = None
    serializer_class = BillboardRequirementSerializer

    def get_queryset(self):
        state = self.kwargs.get('state')
        return BillboardRequirement.objects.filter(state=state)
