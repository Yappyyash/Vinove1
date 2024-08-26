# Generated by Django 5.0.7 on 2024-08-25 05:07

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserActivity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("application", models.CharField(max_length=255)),
                ("start_time", models.DateTimeField()),
                ("usage_time", models.FloatField()),
                ("key_presses", models.IntegerField()),
                ("mouse_clicks", models.IntegerField()),
            ],
        ),
    ]
