# Generated by Django 5.0.1 on 2024-01-26 22:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0002_rename_body_notification_message_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={"ordering": ("created_at",)},
        ),
    ]