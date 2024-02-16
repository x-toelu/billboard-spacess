from cloudinary.models import CloudinaryField
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=225)
    image = CloudinaryField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=225)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

