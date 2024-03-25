from django.urls import path

from .views import (StateBillBoardReqDetailView, StateListView,
                    UploadRequirementView)

urlpatterns = [
    path('upload/', UploadRequirementView.as_view(), name='upload-requirements'),
    path('states/', StateListView.as_view(), name='states-list'),
    path(
        'states/<str:state>/',
        StateBillBoardReqDetailView.as_view(),
        name='state-billboard-requirements'
    ),
]
