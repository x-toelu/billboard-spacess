from django.db import models


class SubscriptionType(models.TextChoices):
    FREE = 'free'
    BASIC = 'basic'
    PRO = 'pro'
