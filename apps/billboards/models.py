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

    # available date range
    available_date_from = models.DateField()
    available_date_to = models.DateField()

    # target audience range
    target_audience_from = models.PositiveIntegerField()
    target_audience_to = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.owner}'s billboard at {self.location}"

    @property
    def target_audience(self):
        return f"{self.target_audience_from} to {self.target_audience_to}"

    @property
    def available_date(self):
        return self.available_date_from - self.available_date_to
