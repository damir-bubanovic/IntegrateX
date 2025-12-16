import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.organizations.models import Membership, Organization


@pytest.mark.django_db
def test_organization_str_returns_name():
    org = Organization.objects.create(name="Acme Inc", slug="acme-inc")
    assert str(org) == "Acme Inc"


@pytest.mark.django_db
def test_membership_default_role_is_member():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="alice", password="pass12345")

    org = Organization.objects.create(name="Org One", slug="org-one")
    m = Membership.objects.create(user=user, organization=org)

    assert m.role == Membership.OrgRole.MEMBER
    assert m.is_active is True


@pytest.mark.django_db
def test_membership_unique_together_user_org():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="bob", password="pass12345")

    org = Organization.objects.create(name="Org Two", slug="org-two")
    Membership.objects.create(user=user, organization=org)

    with pytest.raises(IntegrityError):
        Membership.objects.create(user=user, organization=org)


@pytest.mark.django_db
def test_membership_str_includes_user_org_and_role():
    user_model = get_user_model()
    user = user_model.objects.create_user(username="carol", password="pass12345")

    org = Organization.objects.create(name="Org Three", slug="org-three")
    m = Membership.objects.create(user=user, organization=org, role=Membership.OrgRole.ADMIN)

    s = str(m)
    assert "carol" in s
    assert "Org Three" in s
    assert "admin" in s
