import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


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
    USER_CHOICES = (
        ('billboard_owner', 'Billboard Owner'),
        ('state_agent', 'State Agent'),
        ('advertising_agent', 'Advertising Agent'),
        ('business_owner', 'Business Owner'),
    )
    NIGERIAN_STATES = [
        ('abia', 'Abia'), ('adamawa', 'Adamawa'), ('akwa_ibom', 'Akwa Ibom'),
        ('anambra', 'Anambra'), ('bauchi', 'Bauchi'), ('bayelsa', 'Bayelsa'),
        ('benue', 'Benue'), ('borno', 'Borno'), ('cross_river', 'Cross River'),
        ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('edo', 'Edo'), ('ekiti', 'Ekiti'),
        ('enugu', 'Enugu'), ('gombe', 'Gombe'), ('imo', 'Imo'), ('jigawa', 'Jigawa'),
        ('kaduna', 'Kaduna'), ('kano', 'Kano'), ('katsina', 'Katsina'),
        ('kebbi', 'Kebbi'), ('kogi', 'Kogi'), ('kwara', 'Kwara'), ('lagos', 'Lagos'),
        ('nasarawa', 'Nasarawa'), ('niger', 'Niger'), ('ogun', 'Ogun'),
        ('ondo', 'Ondo'), ('osun', 'Osun'), ('oyo', 'Oyo'), ('plateau', 'Plateau'),
        ('rivers', 'Rivers'), ('sokoto', 'Sokoto'), ('taraba', 'Taraba'),
        ('yobe', 'Yobe'), ('zamfara', 'Zamfara'), ('federal_capital_territory', 'FCT')
    ]

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

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
