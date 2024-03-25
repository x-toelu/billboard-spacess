from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from services.eventbrite import EventBriteService
from utils.constants import EVENTS_STATE_IDS

from .models import Event
from .serializers import EventSerializer


class EventListView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class GetNewEventsView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        eventbrite = EventBriteService()
        queryset = eventbrite.get_events(list(EVENTS_STATE_IDS.values()))
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
