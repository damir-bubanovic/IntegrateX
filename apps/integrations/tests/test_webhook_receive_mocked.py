import json
from typing import Any

import pytest
from rest_framework.test import APIClient

from apps.integrations.models import Integration, WebhookEvent
from apps.organizations.models import Organization
from apps.integrations.webhooks.validators import compute_hmac_sha256_hex


@pytest.mark.django_db
def test_webhook_receive_creates_event_and_enqueues_task(monkeypatch):
    called: dict[str, tuple[Any, ...] | None] = {"args": None}

    class _DummyAsyncResult:
        pass

    def fake_delay(*args: Any, **_kwargs: Any) -> object:
        called["args"] = args
        return _DummyAsyncResult()

    # Patch Celery task enqueue where it is used (delay on the imported task object)
    monkeypatch.setattr("apps.integrations.webhooks.views.process_webhook_event.delay", fake_delay)

    org = Organization.objects.create(name="Org One", slug="org-one")
    integration = Integration.objects.create(
        organization=org,
        provider=Integration.Provider.HTTPBIN,
        name="Webhook Test",
        api_base_url="https://httpbin.org",
        webhook_secret="secret123",
        is_active=True,
    )
    integration_pk = int(integration.pk)

    payload = {"type": "test.event", "data": {"x": 1}}
    raw_body = json.dumps(payload).encode("utf-8")
    signature = compute_hmac_sha256_hex("secret123", raw_body)

    client = APIClient()
    resp = client.post(
        f"/api/v1/integrations/webhooks/{integration_pk}/",
        data=raw_body,
        content_type="application/json",
        HTTP_X_INTEGRATEX_SIGNATURE=signature,
    )

    assert resp.status_code == 202
    assert resp.data["accepted"] is True
    assert "id" in resp.data

    created_event_id = resp.data["id"]
    event = WebhookEvent.objects.get(pk=created_event_id)

    assert int(event.integration.pk) == integration_pk
    assert event.signature_valid is True
    assert event.payload == payload

    assert called["args"] == (created_event_id,)
