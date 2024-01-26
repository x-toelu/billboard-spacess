from django.urls import path

from .views import BillboardCreateView, BillboardDetailView, BillboardListView

urlpatterns = [
    path('all/', BillboardListView.as_view(), name='billboards-list'),
    path('<int:pk>/', BillboardDetailView.as_view(), name='billboards-retrieve'),
    path('create/', BillboardCreateView.as_view(), name='billboards-create'),
]
