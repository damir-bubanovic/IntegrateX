from django.http import Http404
from .models import Organization


class OrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        org_slug = request.headers.get("X-Org-Slug")
        if org_slug:
            # noinspection PyUnresolvedReferences
            try:
                request.organization = Organization.objects.get(slug=org_slug, is_active=True)
            # noinspection PyUnresolvedReferences
            except Organization.DoesNotExist:
                raise Http404("Organization not found")
        else:
            request.organization = None

        return self.get_response(request)
