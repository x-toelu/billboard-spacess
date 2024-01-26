from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Billboard

from apps.notifications.models import Notification


@receiver(post_save, sender=Billboard)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal handler to create notification.
    """
    if created:
        Notification.objects.create(
            user=instance.owner,
            type='congratulations',
            message=f'Billboard uploaded successful for {instance.location}'
        )
