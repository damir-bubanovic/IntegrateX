from django.urls import path
from .views import CurrentOrganizationView, OrgAdminOnlyView

urlpatterns = [
    path("current/", CurrentOrganizationView.as_view(), name="current-organization"),
    path("admin-only/", OrgAdminOnlyView.as_view(), name="org-admin-only"),
]
