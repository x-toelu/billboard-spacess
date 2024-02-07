from cloudinary.models import CloudinaryField
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=225)
    image = CloudinaryField()
    date = models.DateField()
    time = models.TimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
