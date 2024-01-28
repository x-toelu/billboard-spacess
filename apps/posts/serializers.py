from rest_framework import serializers

from .models import Post
from apps.accounts.serializers import MiniUserSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_image(self, obj):
        """Returns full image url"""
        request = self.context.get('request')
        file_url = obj.image.url
        return request.build_absolute_uri(file_url)
