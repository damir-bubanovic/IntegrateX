from rest_framework import serializers
from apps.integrations.models import WebhookEvent


class WebhookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = [
            "id",
            "integration",
            "status",
            "signature_valid",
            "received_at",
            "processed_at",
            "attempts",
            "last_error",
        ]
        read_only_fields = fields


class WebhookEventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookEvent
        fields = [
            "id",
            "integration",
            "status",
            "signature_header",
            "signature_valid",
            "headers",
            "payload",
            "raw_body",
            "received_at",
            "processed_at",
            "attempts",
            "last_error",
        ]
        read_only_fields = fields
