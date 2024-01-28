from rest_framework.generics import ListAPIView, CreateAPIView

from .models import Post
from .serializers import PostListSerializer, PostCreateSerializer


class PostListCreateView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

