import uuid

from django.db import migrations, models


def backfill_fingerprints(apps, _schema_editor):
    webhook_event_model = apps.get_model("integrations", "WebhookEvent")
    # Ensure all existing rows get a non-empty unique fingerprint
    for ev in webhook_event_model.objects.all().only("id", "fingerprint"):
        if not ev.fingerprint:
            ev.fingerprint = uuid.uuid4().hex  # 32 chars, unique enough
            ev.save(update_fields=["fingerprint"])


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0002_webhookevent_state"),
    ]

    operations = [
        # 1) Add nullable field first
        migrations.AddField(
            model_name="webhookevent",
            name="fingerprint",
            field=models.CharField(max_length=64, null=True, blank=True, db_index=True),
        ),
        # 2) Backfill existing rows with unique values
        migrations.RunPython(backfill_fingerprints, migrations.RunPython.noop),
        # 3) Make it non-null with a default (new rows must set a real value in code)
        migrations.AlterField(
            model_name="webhookevent",
            name="fingerprint",
            field=models.CharField(max_length=64, default="", blank=True, db_index=True),
        ),
        # 4) Add uniqueness constraint
        migrations.AddConstraint(
            model_name="webhookevent",
            constraint=models.UniqueConstraint(
                fields=("integration", "fingerprint"),
                name="uniq_webhook_event_fingerprint",
            ),
        ),
    ]
