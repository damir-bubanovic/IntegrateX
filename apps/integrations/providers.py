import requests


class HTTPBinClient:
    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def ping(self) -> dict:
        try:
            r = requests.get(f"{self.base_url}/get", timeout=10)
            r.raise_for_status()
            return {"ok": True, "status_code": r.status_code, "data": r.json()}
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}


def get_client(provider: str, base_url: str, api_key: str = ""):
    if provider == "httpbin":
        return HTTPBinClient(base_url=base_url, api_key=api_key)
    raise ValueError(f"Unknown provider: {provider}")
