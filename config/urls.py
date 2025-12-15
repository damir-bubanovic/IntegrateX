from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import IntegrateXTokenObtainPairView
from apps.users.api_test_views import WhoAmIView, AdminOnlyView


urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("api/v1/auth/token/", IntegrateXTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # User test endpoints
    path("api/v1/me/", WhoAmIView.as_view(), name="me"),
    path("api/v1/admin-only/", AdminOnlyView.as_view(), name="admin-only"),

    # Organization endpoints
    path("api/v1/org/", include("apps.organizations.urls")),
]
