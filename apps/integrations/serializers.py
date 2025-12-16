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

    def validate_provider(self, value: str) -> str:
        allowed = {c[0] for c in Integration.Provider.choices}
        if value not in allowed:
            raise serializers.ValidationError("Unsupported provider")
        return value
