from django.http import Http404
from .models import Organization


class OrganizationMiddleware:
    """
    Resolves current organization from X-Org-Slug header.
    Attaches request.organization (or None if missing).
    Auth/membership enforcement happens in DRF permissions (JWT runs there).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        org_slug = request.headers.get("X-Org-Slug")
        request.organization = None

        if org_slug:
            try:
                request.organization = Organization.objects.get(slug=org_slug, is_active=True)
            except Organization.DoesNotExist:
                raise Http404("Organization not found")

        return self.get_response(request)
