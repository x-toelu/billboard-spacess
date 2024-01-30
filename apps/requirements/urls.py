from django.urls import path

from .views import StateBillBoardReqDetailView, StateListView

urlpatterns = [
    path('states/', StateListView.as_view(), name='states-list'),
    path(
        'states/<str:state>/',
        StateBillBoardReqDetailView.as_view(),
        name='state-billboard-requirements'
    ),
]
