# Generated by Django 5.0.1 on 2024-02-08 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_delete_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="country",
            field=models.CharField(
                choices=[("NG", "Nigeria")], default="NG", max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="display_name",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="full_name",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="state_of_residence",
            field=models.CharField(
                choices=[
                    ("abia", "Abia"),
                    ("adamawa", "Adamawa"),
                    ("akwa-ibom", "Akwa Ibom"),
                    ("anambra", "Anambra"),
                    ("bauchi", "Bauchi"),
                    ("bayelsa", "Bayelsa"),
                    ("benue", "Benue"),
                    ("borno", "Borno"),
                    ("cross-river", "Cross River"),
                    ("delta", "Delta"),
                    ("ebonyi", "Ebonyi"),
                    ("edo", "Edo"),
                    ("ekiti", "Ekiti"),
                    ("enugu", "Enugu"),
                    ("fct", "Fct"),
                    ("gombe", "Gombe"),
                    ("imo", "Imo"),
                    ("jigawa", "Jigawa"),
                    ("kaduna", "Kaduna"),
                    ("kano", "Kano"),
                    ("katsina", "Katsina"),
                    ("kebbi", "Kebbi"),
                    ("kogi", "Kogi"),
                    ("kwara", "Kwara"),
                    ("lagos", "Lagos"),
                    ("nasarawa", "Nasarawa"),
                    ("niger", "Niger"),
                    ("ogun", "Ogun"),
                    ("ondo", "Ondo"),
                    ("osun", "Osun"),
                    ("oyo", "Oyo"),
                    ("plateau", "Plateau"),
                    ("rivers", "Rivers"),
                    ("sokoto", "Sokoto"),
                    ("taraba", "Taraba"),
                    ("yobe", "Yobe"),
                    ("zamfara", "Zamfara"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="user_field",
            field=models.CharField(
                choices=[
                    ("billboard-owner", "Billboard Owner"),
                    ("state-agent", "State Agent"),
                    ("advertising-agent", "Advertising Agent"),
                    ("business-owner", "Business Owner"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]