import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
class TestAuthAndRBAC:
    def test_token_obtain_pair_returns_tokens_and_custom_claims(self):
        user_model = get_user_model()
        user_model.objects.create_user(
            username="alice",
            password="pass12345",
            role=user_model.Role.USER,
        )

        client = APIClient()
        resp = client.post(
            "/api/v1/auth/token/",
            {"username": "alice", "password": "pass12345"},
            format="json",
        )

        assert resp.status_code == 200
        assert "access" in resp.data
        assert "refresh" in resp.data

        access = resp.data["access"]
        token = AccessToken(access)
        assert token["username"] == "alice"
        assert token["role"] == "user"

    def test_me_requires_auth(self):
        client = APIClient()
        resp = client.get("/api/v1/me/")
        # With SessionAuthentication enabled, DRF may return 401 or 403
        assert resp.status_code in (401, 403)

    def test_me_returns_user_payload_when_authenticated(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="bob",
            password="pass12345",
            role=user_model.Role.MANAGER,
        )

        client = APIClient()
        client.force_authenticate(user=user)

        resp = client.get("/api/v1/me/")
        assert resp.status_code == 200
        assert resp.data["id"] == user.id
        assert resp.data["username"] == "bob"
        assert resp.data["role"] == "manager"

    def test_admin_only_requires_auth(self):
        client = APIClient()
        resp = client.get("/api/v1/admin-only/")
        assert resp.status_code in (401, 403)

    def test_admin_only_forbids_non_admin(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="carol",
            password="pass12345",
            role=user_model.Role.USER,
        )

        client = APIClient()
        client.force_authenticate(user=user)

        resp = client.get("/api/v1/admin-only/")
        assert resp.status_code == 403

    def test_admin_only_allows_admin(self):
        user_model = get_user_model()
        admin = user_model.objects.create_user(
            username="admin1",
            password="pass12345",
            role=user_model.Role.ADMIN,
        )

        client = APIClient()
        client.force_authenticate(user=admin)

        resp = client.get("/api/v1/admin-only/")
        assert resp.status_code == 200
        assert resp.data["ok"] is True
        assert "admin1" in resp.data["message"]
