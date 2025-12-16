import sys
from django.urls import path, include

from .views import CurrentOrganizationView, OrgAdminOnlyView

urlpatterns = [
    path("current/", CurrentOrganizationView.as_view(), name="current-organization"),
    path("admin-only/", OrgAdminOnlyView.as_view(), name="org-admin-only"),
]

# Test-only endpoints (enabled only when running pytest)
if "pytest" in sys.modules:
    urlpatterns += [
        path("", include("apps.organizations.tests.test_urls")),
    ]
