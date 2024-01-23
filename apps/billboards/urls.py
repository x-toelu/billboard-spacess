from django.urls import path

from .views import BillboardListView

urlpatterns = [
    path('', BillboardListView.as_view(), name='billboards-list')
]
