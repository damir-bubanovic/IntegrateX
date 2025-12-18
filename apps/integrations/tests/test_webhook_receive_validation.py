import json

import pytest
from rest_framework.test import APIClient

from apps.integrations.models import Integration, WebhookEvent
from apps.organizations.models import Organization
from apps.integrations.webhooks.validators import compute_hmac_sha256_hex


@pytest.mark.django_db
def test_webhook_missing_signature_returns_400():
    org = Organization.objects.create(name="Org One", slug="org-one")
    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="Webhook Test",
        api_base_url="https://httpbin.org",
        webhook_secret="secret123",
        is_active=True,
    )

    client = APIClient()
    resp = client.post(
        f"/api/v1/integrations/webhooks/{int(integration.pk)}/",
        data=b'{"type":"x"}',
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert resp.data["accepted"] is False


@pytest.mark.django_db
def test_webhook_invalid_json_returns_400():
    org = Organization.objects.create(name="Org One", slug="org-one")
    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="Webhook Test",
        api_base_url="https://httpbin.org",
        webhook_secret="secret123",
        is_active=True,
    )

    raw = b'{"type":'  # invalid JSON
    sig = compute_hmac_sha256_hex("secret123", raw)

    client = APIClient()
    resp = client.post(
        f"/api/v1/integrations/webhooks/{int(integration.pk)}/",
        data=raw,
        content_type="application/json",
        HTTP_X_INTEGRATEX_SIGNATURE=sig,
    )
    assert resp.status_code == 400
    assert resp.data["accepted"] is False


@pytest.mark.django_db
def test_webhook_non_object_json_returns_400():
    org = Organization.objects.create(name="Org One", slug="org-one")
    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="Webhook Test",
        api_base_url="https://httpbin.org",
        webhook_secret="secret123",
        is_active=True,
    )

    raw = json.dumps(["not", "an", "object"]).encode("utf-8")
    sig = compute_hmac_sha256_hex("secret123", raw)

    client = APIClient()
    resp = client.post(
        f"/api/v1/integrations/webhooks/{int(integration.pk)}/",
        data=raw,
        content_type="application/json",
        HTTP_X_INTEGRATEX_SIGNATURE=sig,
    )
    assert resp.status_code == 400
    assert resp.data["accepted"] is False


@pytest.mark.django_db
def test_webhook_payload_too_large_returns_413():
    org = Organization.objects.create(name="Org One", slug="org-one")
    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="Webhook Test",
        api_base_url="https://httpbin.org",
        webhook_secret="secret123",
        is_active=True,
    )

    raw = b"a" * (256 * 1024 + 1)  # 256KB + 1
    sig = compute_hmac_sha256_hex("secret123", raw)

    client = APIClient()
    resp = client.post(
        f"/api/v1/integrations/webhooks/{int(integration.pk)}/",
        data=raw,
        content_type="application/json",
        HTTP_X_INTEGRATEX_SIGNATURE=sig,
    )
    assert resp.status_code == 413
    assert resp.data["accepted"] is False
    assert WebhookEvent.objects.count() == 0
