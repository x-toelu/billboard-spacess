from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView, Response

from .models import BillboardRequirement
from .serializers import BillboardRequirementSerializer


class StateBillBoardReqDetailView(ListAPIView):
    serializer_class = BillboardRequirementSerializer

    def get_queryset(self):
        state = self.kwargs.get('state')
        return BillboardRequirement.objects.filter(state=state)


class StateListView(APIView):
    def get(self, request, format=None):
        states = (
            BillboardRequirement.objects
            .values_list('state', flat=True)
            .distinct()
        )

        state_list = []
        for state in states:
            name = state.lower()
            url = reverse(
                'state-billboard-requirements',
                kwargs={'state': name},
                request=request,
                format=format
            )

            data = {'name': name, 'url': url}
            state_list.append(data)

        return Response(state_list)


class UploadRequirementView(CreateAPIView):
    serializer_class = BillboardRequirementSerializer

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
