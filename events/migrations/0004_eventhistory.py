# Generated by Django 2.1.5 on 2019-01-07 15:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [("events", "0003_event_status")]

    operations = [
        migrations.CreateModel(
            name="EventHistory",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("response", django.contrib.postgres.fields.jsonb.JSONField()),
                (
                    "status",
                    models.CharField(
                        choices=[("success", "success"), ("error", "error")],
                        max_length=20,
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_history",
                        to="events.Event",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]