from django.urls import path

from .views import (
    BillboardCreateView,
    BillboardDetailView,
    BillboardListView,
    BillboardListByCategoryAPIView,
    NewlyAddedBillboardListView,
)

urlpatterns = [
    path('all/', BillboardListView.as_view(), name='billboards-list'),
    path('<int:pk>/', BillboardDetailView.as_view(), name='billboards-retrieve'),
    path('create/', BillboardCreateView.as_view(), name='billboards-create'),
    path('new/', NewlyAddedBillboardListView.as_view(), name='billboards-new'),
    path(
        'billboardscategory/<str:category>/',
        BillboardListByCategoryAPIView.as_view(),
        name='billboard-list-by-category'
    )
]
