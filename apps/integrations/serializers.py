from urllib.parse import urlparse

from rest_framework import serializers

from .models import Integration


class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = (
            "id",
            "provider",
            "name",
            "is_active",
            "api_base_url",
            "api_key",
            "created_at",
        )
        read_only_fields = ("id", "created_at")

    @staticmethod
    def validate_provider(value: str) -> str:
        allowed = {c[0] for c in Integration.Provider.choices}
        if value not in allowed:
            raise serializers.ValidationError("Unsupported provider")
        return value

    @staticmethod
    def validate_name(value: str) -> str:
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("Name is required")
        if len(v) > 100:
            raise serializers.ValidationError("Name too long (max 100)")
        return v

    @staticmethod
    def validate_api_base_url(value: str) -> str:
        v = (value or "").strip()
        if not v:
            raise serializers.ValidationError("api_base_url is required")

        parsed = urlparse(v)
        if parsed.scheme not in {"http", "https"}:
            raise serializers.ValidationError("api_base_url must start with http:// or https://")
        if not parsed.netloc:
            raise serializers.ValidationError("api_base_url must be a valid URL")

        # Normalize: remove trailing slash for consistent URL joining
        return v.rstrip("/")

    @staticmethod
    def validate_api_key(value: str) -> str:
        # Allow blank keys (some providers might not require it)
        v = (value or "").strip()
        if len(v) > 512:
            raise serializers.ValidationError("api_key too long (max 512)")
        return v
