from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    NOTIF_TYPES = (
        ('congratulations', 'congratulations'),
        ('maintenance', 'maintenance'),
        ('explore', 'explore'),
    )

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    type = models.CharField(max_length=15, choices=NOTIF_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        self.is_read = True
        self.save()

