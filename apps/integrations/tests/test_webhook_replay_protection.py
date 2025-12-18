import json
from typing import Any

import pytest
from rest_framework.test import APIClient

from apps.integrations.models import Integration, WebhookEvent
from apps.organizations.models import Organization
from apps.integrations.webhooks.validators import compute_hmac_sha256_hex


@pytest.mark.django_db
def test_webhook_replay_returns_200_and_does_not_enqueue_twice(monkeypatch):
    calls: dict[str, int] = {"count": 0}

    class _DummyAsyncResult:
        pass

    def fake_delay(*args: Any, **_kwargs: Any) -> object:
        calls["count"] += 1
        return _DummyAsyncResult()

    monkeypatch.setattr("apps.integrations.webhooks.views.process_webhook_event.delay", fake_delay)

    org = Organization.objects.create(name="Org One", slug="org-one")
    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="Webhook Replay Test",
        api_base_url="https://httpbin.org",
        webhook_secret="secret123",
        is_active=True,
    )

    payload = {"type": "test.event", "data": {"x": 1}}
    raw_body = json.dumps(payload).encode("utf-8")
    sig = compute_hmac_sha256_hex("secret123", raw_body)

    client = APIClient()

    r1 = client.post(
        f"/api/v1/integrations/webhooks/{int(integration.pk)}/",
        data=raw_body,
        content_type="application/json",
        HTTP_X_INTEGRATEX_SIGNATURE=sig,
    )
    assert r1.status_code == 202
    assert calls["count"] == 1
    assert WebhookEvent.objects.count() == 1

    r2 = client.post(
        f"/api/v1/integrations/webhooks/{int(integration.pk)}/",
        data=raw_body,
        content_type="application/json",
        HTTP_X_INTEGRATEX_SIGNATURE=sig,
    )
    assert r2.status_code == 200
    assert r2.data["accepted"] is True
    assert r2.data.get("replay") is True
    assert calls["count"] == 1
    assert WebhookEvent.objects.count() == 1
