import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.constants import NIGERIAN_STATES, USER_CHOICES


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    username = None
    email = models.EmailField(_("email address"), max_length=100, unique=True)
    user_field = models.CharField(
        max_length=20, choices=USER_CHOICES, blank=True, null=True
    )
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    state_of_residence = models.CharField(
        max_length=255, choices=NIGERIAN_STATES, blank=True, null=True
    )
    display_name = models.CharField(max_length=255, blank=True, null=True)

    # for password reset
    password_reset_otp = models.CharField(max_length=6, null=True)
    password_reset_otp_created_at = models.DateTimeField(null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
