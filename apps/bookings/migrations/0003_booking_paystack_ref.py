# Generated by Django 5.0.1 on 2024-02-02 22:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0002_booking_paid"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="paystack_ref",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
