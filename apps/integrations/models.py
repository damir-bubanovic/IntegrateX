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

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "provider", "name")

    def __str__(self) -> str:
        return f"{str(self.organization)}:{self.provider}:{self.name}"

