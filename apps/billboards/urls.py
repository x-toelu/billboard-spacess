from django.urls import path

from .views import BillboardListView, BillboardCreateView

urlpatterns = [
    path('', BillboardListView.as_view(), name='billboards-list'),
    path('create/', BillboardCreateView.as_view(), name='billboards-create'),
]
