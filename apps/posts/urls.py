from django.urls import path

from .views import PostListCreateView, PostCreateView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('create/', PostCreateView.as_view(), name='post-create'),
]
