import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.organizations.models import Membership, Organization


@pytest.mark.django_db
class TestOrganizationPermissions:
    def setup_method(self):
        self.client = APIClient()
        user_model = get_user_model()

        self.member = user_model.objects.create_user(username="member1", password="pass12345")
        self.org_admin = user_model.objects.create_user(username="orgadmin1", password="pass12345")
        self.other_org_member = user_model.objects.create_user(username="other1", password="pass12345")

        self.org = Organization.objects.create(name="Org One", slug="org-one")
        self.other_org = Organization.objects.create(name="Org Two", slug="org-two")

        Membership.objects.create(
            user=self.member,
            organization=self.org,
            role=Membership.OrgRole.MEMBER,
            is_active=True,
        )
        Membership.objects.create(
            user=self.org_admin,
            organization=self.org,
            role=Membership.OrgRole.ADMIN,
            is_active=True,
        )
        Membership.objects.create(
            user=self.other_org_member,
            organization=self.other_org,
            role=Membership.OrgRole.MEMBER,
            is_active=True,
        )

    def test_current_requires_org_header(self):
        self.client.force_authenticate(user=self.member)
        resp = self.client.get("/api/v1/org/current/")
        assert resp.status_code == 403  # HasOrganization fails

    def test_current_rejects_user_not_in_org(self):
        self.client.force_authenticate(user=self.other_org_member)
        resp = self.client.get(
            "/api/v1/org/current/",
            HTTP_X_ORG_SLUG="org-one",
        )
        assert resp.status_code == 403  # IsOrgMember fails

    def test_current_allows_member(self):
        self.client.force_authenticate(user=self.member)
        resp = self.client.get(
            "/api/v1/org/current/",
            HTTP_X_ORG_SLUG="org-one",
        )
        assert resp.status_code == 200
        assert resp.data["organization"]["slug"] == "org-one"
        assert resp.data["organization"]["name"] == "Org One"

    def test_admin_only_forbids_non_admin_member(self):
        self.client.force_authenticate(user=self.member)
        resp = self.client.get(
            "/api/v1/org/admin-only/",
            HTTP_X_ORG_SLUG="org-one",
        )
        assert resp.status_code == 403  # IsOrgAdmin fails

    def test_admin_only_allows_org_admin(self):
        self.client.force_authenticate(user=self.org_admin)
        resp = self.client.get(
            "/api/v1/org/admin-only/",
            HTTP_X_ORG_SLUG="org-one",
        )
        assert resp.status_code == 200
        assert resp.data["ok"] is True
        assert resp.data["org"] == "org-one"
