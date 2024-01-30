from django.urls import path

from .views import StateBillBoardRequirementListView

urlpatterns = [
    path(
        '<str:state>/',
        StateBillBoardRequirementListView.as_view(),
        name='billboard-requirements-list'
    ),

]
