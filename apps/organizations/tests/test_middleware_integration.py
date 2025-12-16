import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.organizations.models import Organization


@pytest.mark.django_db
class TestOrganizationMiddleware:
    def setup_method(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username="alice",
            password="pass12345",
        )
        self.client.force_authenticate(user=self.user)

    def test_request_without_org_header_sets_none(self):
        resp = self.client.get("/api/v1/org/test-org-context/")
        assert resp.status_code == 200
        assert resp.data["org"] is None

    def test_valid_org_slug_resolves_organization(self):
        Organization.objects.create(name="Acme", slug="acme")

        resp = self.client.get(
            "/api/v1/org/test-org-context/",
            HTTP_X_ORG_SLUG="acme",
        )

        assert resp.status_code == 200
        assert resp.data["org"] == "acme"

    def test_invalid_org_slug_returns_404(self):
        resp = self.client.get(
            "/api/v1/org/test-org-context/",
            HTTP_X_ORG_SLUG="does-not-exist",
        )
        assert resp.status_code == 404
