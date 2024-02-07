from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.subscriptions.models import Subscription


@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Signal handler to send verification email to a new user.
    """
    if created:
        Subscription.objects.create(user=instance)

        send_mail(
            'Welcome to Billboard Spaces',
            'Hello, We are glad to have you here.',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False
        )
