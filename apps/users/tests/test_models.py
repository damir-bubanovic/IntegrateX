import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_user_default_role_is_user():
    user_model = get_user_model()
    u = user_model.objects.create_user(
        username="alice",
        password="pass12345",
    )
    assert u.role == user_model.Role.USER


@pytest.mark.django_db
def test_user_role_can_be_admin():
    user_model = get_user_model()
    u = user_model.objects.create_user(
        username="admin1",
        password="pass12345",
        role=user_model.Role.ADMIN,
    )
    assert u.role == user_model.Role.ADMIN


@pytest.mark.django_db
def test_user_str_includes_username_and_role():
    user_model = get_user_model()
    u = user_model.objects.create_user(
        username="bob",
        password="pass12345",
        role=user_model.Role.MANAGER,
    )
    s = str(u)
    assert "bob" in s
    assert "manager" in s
