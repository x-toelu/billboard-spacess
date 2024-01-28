from cloudinary.models import CloudinaryField

from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        related_name='posts',
        on_delete=models.CASCADE
    )

    caption = models.CharField(max_length=500, null=True)
    image = CloudinaryField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
