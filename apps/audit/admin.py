from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "organization", "action", "method", "path", "status_code")
    list_filter = ("action", "method", "status_code", "organization")
    search_fields = ("path", "actor__username", "metadata", "user_agent")
    ordering = ("-created_at",)
