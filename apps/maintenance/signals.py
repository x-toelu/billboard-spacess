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
    superuser_emails = superusers.values_list('email', flat=True)

    if created:
        message = f"""
        {instance.user.display_name} would like a maintenace on
        {instance.preferred_date} at {instance.preferred_date} beacause; {instance.description}
        """
        send_mail(
            f'{instance.user.display_name} booked for maintenance',
            message,
            settings.DEFAULT_FROM_EMAIL,
            superuser_emails,
            fail_silently=False
        )
