from django.urls import path
from .views import IntegrationListCreateView, IntegrationPingView

urlpatterns = [
    path("", IntegrationListCreateView.as_view(), name="integration-list-create"),
    path("<int:integration_id>/ping/", IntegrationPingView.as_view(), name="integration-ping"),
]
