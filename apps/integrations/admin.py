from django.contrib import admin
from .models import Integration

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "provider", "name", "is_active", "created_at")
    list_filter = ("provider", "is_active")
    search_fields = ("name", "organization__slug")
