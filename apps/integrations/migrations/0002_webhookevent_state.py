import uuid

import django.db.models.deletion
from django.db import migrations, models
from django.utils import timezone


WEBHOOK_EVENT_FIELDS = [
    (
        "id",
        models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False,
            serialize=False,
        ),
    ),
    (
        "integration",
        models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE,
            related_name="webhook_events",
            to="integrations.integration",
        ),
    ),
    (
        "status",
        models.CharField(
            max_length=20,
            choices=[
                ("received", "Received"),
                ("processing", "Processing"),
                ("succeeded", "Succeeded"),
                ("failed", "Failed"),
            ],
            default="received",
        ),
    ),
    ("signature_header", models.CharField(max_length=255, blank=True, default="")),
    ("signature_valid", models.BooleanField(default=False)),
    ("headers", models.JSONField(default=dict, blank=True)),
    ("payload", models.JSONField(default=dict, blank=True)),
    ("raw_body", models.TextField(blank=True, default="")),
    ("received_at", models.DateTimeField(default=timezone.now)),
    ("processed_at", models.DateTimeField(null=True, blank=True)),
    ("attempts", models.PositiveIntegerField(default=0)),
    ("last_error", models.TextField(blank=True, default="")),
]


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            # For a fresh DB (pytest), actually create the table.
            database_operations=[
                migrations.CreateModel(
                    name="WebhookEvent",
                    fields=WEBHOOK_EVENT_FIELDS,
                    options={},
                )
            ],
            # Keep migration state consistent.
            state_operations=[
                migrations.CreateModel(
                    name="WebhookEvent",
                    fields=WEBHOOK_EVENT_FIELDS,
                    options={},
                )
            ],
        ),
    ]
