# Generated by Django 5.0.1 on 2024-01-29 19:10

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("billboards", "0007_billboard_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="billboard",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.00"), max_digits=20
            ),
        ),
        migrations.AlterField(
            model_name="billboard",
            name="is_verified",
            field=models.BooleanField(default=True),
        ),
    ]
