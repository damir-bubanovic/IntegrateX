from django.db import models
from apps.organizations.models import Organization


class Integration(models.Model):
    class Provider(models.TextChoices):
        HTTPBIN = "httpbin", "HTTPBin (Demo)"

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="integrations")
    provider = models.CharField(max_length=50, choices=Provider.choices)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # demo “config”
    api_base_url = models.URLField(default="https://httpbin.org")
    api_key = models.CharField(max_length=255, blank=True, default="")

    webhook_secret = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "provider", "name")

    def __str__(self) -> str:
        return f"{str(self.organization)}:{self.provider}:{self.name}"




import uuid
from django.utils import timezone

class WebhookEvent(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Received"
        PROCESSING = "processing", "Processing"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    integration = models.ForeignKey(
        Integration,
        on_delete=models.CASCADE,
        related_name="webhook_events",
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RECEIVED)

    signature_header = models.CharField(max_length=255, blank=True, default="")
    signature_valid = models.BooleanField(default=False)

    headers = models.JSONField(default=dict, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    raw_body = models.TextField(blank=True, default="")

    received_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)

    attempts = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True, default="")

    def __str__(self) -> str:
        return f"{self.integration.id}:{self.id}:{self.status}"

