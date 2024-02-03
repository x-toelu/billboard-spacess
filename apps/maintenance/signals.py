from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MaintenanceBooking


@receiver(post_save, sender=MaintenanceBooking)
def send_maintenance_email(sender, instance, created, **kwargs):
    """
    Alert admins about maintenance booking through email.
    """
    superusers = get_user_model().objects.filter(is_staff=True)

    if created:
        send_mail(
            f'{instance.user.display_name} booked for maintenance',
            '...',
            settings.DEFAULT_FROM_EMAIL,
            [superusers],
            fail_silently=False
        )
