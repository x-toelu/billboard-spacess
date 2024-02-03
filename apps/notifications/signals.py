
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.billboards.models import Billboard
from apps.maintenance.models import MaintenanceBooking

from .models import Notification


@receiver(post_save, sender=Billboard)
def new_billboard_notif(sender, instance, created, **kwargs):
    """
    Create notification when user uploads a billboard.
    """
    if created:
        Notification.objects.create(
            user=instance.owner,
            type='congratulations',
            message=f'Billboard uploaded successful for {instance.full_location}'
        )


@receiver(post_save, sender=MaintenanceBooking)
def new_maintenance_booking_notif(sender, instance, created, **kwargs):
    """
    Create nofication when user books for maintenance.
    """
    if created:
        Notification.objects.create(
            user=instance.owner,
            type='congratulations',
            message=f'Maintenance booking successful for {instance.full_location}'
        )
