from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source="actor.username", read_only=True)
    organization_slug = serializers.CharField(source="organization.slug", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "created_at",
            "action",
            "method",
            "path",
            "status_code",
            "actor",
            "actor_username",
            "organization",
            "organization_slug",
            "ip_address",
            "user_agent",
            "metadata",
        ]
        read_only_fields = fields
