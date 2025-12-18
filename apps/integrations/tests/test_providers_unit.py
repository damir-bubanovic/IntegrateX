import requests

from apps.integrations.providers import HTTPBinClient


class _FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {"hello": "world"}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._payload


def test_httpbin_client_ping_success(monkeypatch):
    def fake_get(_url, **kwargs):
        assert _url.endswith("/get")
        assert kwargs["timeout"] == 10
        return _FakeResponse(status_code=200, payload={"pong": True})

    monkeypatch.setattr("apps.integrations.providers.requests.get", fake_get)

    client = HTTPBinClient(base_url="https://httpbin.org")
    data = client.ping()

    assert data["ok"] is True
    assert data["status_code"] == 200
    assert data["data"] == {"pong": True}


def test_httpbin_client_ping_failure(monkeypatch):
    def fake_get(_url, **kwargs):
        _ = kwargs  # keep linters quiet
        raise requests.RequestException("network down")

    monkeypatch.setattr("apps.integrations.providers.requests.get", fake_get)

    client = HTTPBinClient(base_url="https://httpbin.org")
    data = client.ping()

    assert data["ok"] is False
    assert "error" in data
