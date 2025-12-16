from django.urls import path
from .views import (
    WebhookReceiveView,
    WebhookEventReplayView,
    WebhookEventListView,
    WebhookEventDetailView,
)

urlpatterns = [
    # Receive webhook (public)
    path("<int:integration_id>/", WebhookReceiveView.as_view(), name="webhook-receive"),

    # Manage/view events (authenticated)
    path("<int:integration_id>/events/", WebhookEventListView.as_view(), name="webhook-event-list"),
    path("events/<uuid:id>/", WebhookEventDetailView.as_view(), name="webhook-event-detail"),

    # Replay (admin-only)
    path("events/<uuid:event_id>/replay/", WebhookEventReplayView.as_view(), name="webhook-event-replay"),
]
