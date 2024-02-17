from django.urls import path

from .views import EventDetailView, EventListView, GetNewEventsView

urlpatterns = [
    path('', EventListView.as_view(), name='events-list'),
    path('new/', GetNewEventsView.as_view(), name='new-events'),
    path('<int:pk>/', EventDetailView.as_view(), name='events-detail'),
]
