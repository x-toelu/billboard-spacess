from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models


class Billboard(models.Model):
    SIZE_CHOICES = (
        ('potrait', 'Potrait'),
        ('large_format', 'Large Format'),
        ('48_sheet', '48 Sheet'),
        ('spectacular_billboard', 'Spectacular Billboard'),
        ('gantry', 'Gantry'),
        ('unipole', 'Unipole'),
    )

    owner = models.ForeignKey(
        get_user_model(),
        related_name='billboards',
        on_delete=models.CASCADE
    )
    image = CloudinaryField()
    size = models.CharField(max_length=21, choices=SIZE_CHOICES)
    location = models.CharField(max_length=255)
    target_audience = models.CharField(max_length=255)

    booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.owner.display_name}'s billboard at {self.location}"

