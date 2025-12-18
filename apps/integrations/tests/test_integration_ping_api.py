import pytest
import requests
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.organizations.models import Membership, Organization
from apps.integrations.models import Integration


class _FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {"pong": True}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._payload


@pytest.mark.django_db
def test_integration_ping_api_success(monkeypatch):
    def fake_get(_url, **kwargs):
        assert _url == "https://httpbin.org/get"
        assert kwargs["timeout"] == 10
        return _FakeResponse(status_code=200, payload={"pong": True})

    monkeypatch.setattr("apps.integrations.providers.requests.get", fake_get)

    user_model = get_user_model()
    user = user_model.objects.create_user(username="member1", password="pass12345")

    org = Organization.objects.create(name="Org One", slug="org-one")
    Membership.objects.create(user=user, organization=org, role=Membership.OrgRole.MEMBER, is_active=True)

    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="HTTPBin Demo",
        api_base_url="https://httpbin.org",
        api_key="",
        is_active=True,
    )
    integration_pk = int(integration.pk)

    client = APIClient()
    client.force_authenticate(user=user)

    resp = client.post(
        f"/api/v1/integrations/{integration_pk}/ping/",
        {},
        format="json",
        HTTP_X_ORG_SLUG="org-one",
    )

    assert resp.status_code == 200
    assert resp.data["ok"] is True
    assert resp.data["provider"] == "httpbin"
    assert resp.data["integration"]["id"] == integration_pk
    assert resp.data["integration"]["name"] == "HTTPBin Demo"
    assert resp.data["data"]["ok"] is True
    assert resp.data["data"]["data"] == {"pong": True}
