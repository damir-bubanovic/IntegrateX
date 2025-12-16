from __future__ import annotations

from django.utils.deprecation import MiddlewareMixin
from django.db import transaction

from .models import AuditLog


def _get_client_ip(request) -> str | None:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class AuditMiddleware(MiddlewareMixin):
    """
    Records API requests into AuditLog.
    - Logs authenticated and anonymous requests
    - Focuses on /api/ paths
    - Logs unsafe methods by default, and also logs auth endpoints
    """

    API_PREFIX = "/api/"
    ALWAYS_LOG_PATH_PREFIXES = ("/api/v1/auth/",)

    def process_response(self, request, response):
        path = getattr(request, "path", "") or ""
        method = getattr(request, "method", "") or ""

        if not path.startswith(self.API_PREFIX):
            return response

        should_log = (method in ("POST", "PUT", "PATCH", "DELETE")) or path.startswith(self.ALWAYS_LOG_PATH_PREFIXES)
        if not should_log:
            return response

        actor = getattr(request, "user", None)
        if actor is not None and not getattr(actor, "is_authenticated", False):
            actor = None

        org = getattr(request, "organization", None)

        # Keep metadata intentionally small (no full request body by default).
        metadata = {
            "query_params": dict(getattr(request, "GET", {})),
        }

        # Ensure audit log write doesn’t break the request.
        try:
            with transaction.atomic():
                AuditLog.objects.create(
                    actor=actor,
                    organization=org,
                    action="api.request",
                    method=method,
                    path=path,
                    status_code=getattr(response, "status_code", None),
                    ip_address=_get_client_ip(request),
                    user_agent=request.META.get("HTTP_USER_AGENT", "") or "",
                    metadata=metadata,
                )
        except Exception:
            # Intentionally swallow to avoid interfering with API responses
            pass

        return response
