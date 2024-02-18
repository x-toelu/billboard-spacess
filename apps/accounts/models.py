import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import Country, State, UserField
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    username = None
    email = models.EmailField(_("email address"), max_length=100, unique=True)

    # profile requirements
    user_field = models.CharField(
        max_length=20,
        choices=UserField.choices,
        null=True,
    )
    full_name = models.CharField(max_length=150, null=True)
    display_name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    country = models.CharField(
        max_length=10,
        choices=Country.choices,
        default=Country.NIGERIA
    )
    state = models.CharField(
        max_length=20,
        choices=State.choices,
        null=True
    )

    # Password reset rqeuirements
    password_reset_otp = models.CharField(max_length=6, null=True)
    password_reset_otp_created_at = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.display_name)

