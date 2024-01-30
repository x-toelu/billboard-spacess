from django.urls import path

from .views import StateBillBoardRequirementListView, StateListView

urlpatterns = [
    path('states/', StateListView.as_view(), name='states-list'),
    path(
        'states/<str:state>/',
        StateBillBoardRequirementListView.as_view(),
        name='state-billboard-requirements'
    ),
]
