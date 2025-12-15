from rest_framework.permissions import BasePermission
from .models import Membership


class HasOrganization(BasePermission):
    def has_permission(self, request, view):
        return bool(getattr(request, "organization", None))


class IsOrgMember(BasePermission):
    def has_permission(self, request, view):
        org = getattr(request, "organization", None)
        if not org or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(
            user=request.user,
            organization=org,
            is_active=True,
        ).exists()


class IsOrgAdmin(BasePermission):
    def has_permission(self, request, view):
        org = getattr(request, "organization", None)
        if not org or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(
            user=request.user,
            organization=org,
            is_active=True,
            role="admin",
        ).exists()


class IsOrgManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        org = getattr(request, "organization", None)
        if not org or not request.user.is_authenticated:
            return False
        return Membership.objects.filter(
            user=request.user,
            organization=org,
            is_active=True,
            role__in=("admin", "manager"),
        ).exists()
