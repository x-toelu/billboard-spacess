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
    if created:
        admins = get_user_model().objects.filter(is_staff=True)
        admins_emails = admins.values_list('email', flat=True)

        message = f"""
        {instance.user.display_name} would like a maintenace on {instance.preferred_date}
        {instance.preferred_time} at {instance.location}.
        Reason: {instance.description}
        """
        send_mail(
            subject=f'{instance.user.display_name} booked for maintenance',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admins_emails,
            fail_silently=False
        )
