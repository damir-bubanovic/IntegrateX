from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0003_webhookevent_fingerprint"),
    ]

    operations = [
        migrations.AddField(
            model_name="integration",
            name="webhook_secret",
            field=models.CharField(max_length=255, blank=True, default=""),
        ),
    ]
