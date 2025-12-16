from django.urls import path, include
from .views import IntegrationListCreateView, IntegrationPingView

urlpatterns = [
    path("", IntegrationListCreateView.as_view(), name="integration-list-create"),
    path("<int:integration_id>/ping/", IntegrationPingView.as_view(), name="integration-ping"),
    path("webhooks/", include("apps.integrations.webhooks.urls")),
]
