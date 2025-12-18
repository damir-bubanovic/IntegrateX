import json

from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.integrations.models import Integration, WebhookEvent
from apps.integrations.webhooks.serializers import WebhookEventSerializer, WebhookEventDetailSerializer
from apps.integrations.webhooks.tasks import process_webhook_event
from apps.integrations.webhooks.validators import verify_signature

SIGNATURE_HEADER = "HTTP_X_INTEGRATEX_SIGNATURE"


class WebhookReceiveView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "webhook"

    @staticmethod
    def post(request, integration_id: int):
        integration = Integration.objects.get(id=integration_id, is_active=True)

        raw_body: bytes = request.body or b""
        signature = request.META.get(SIGNATURE_HEADER, "")

        secret = integration.webhook_secret or ""
        is_valid, _expected = verify_signature(secret=secret, body=raw_body, signature_header=signature)

        payload = {}
        if raw_body:
            try:
                payload = json.loads(raw_body.decode("utf-8"))
            except json.JSONDecodeError:
                payload = {}

        event = WebhookEvent.objects.create(
            integration=integration,
            signature_header=signature,
            signature_valid=is_valid,
            headers={k: str(v) for k, v in request.headers.items()},
            payload=payload,
            raw_body=raw_body.decode("utf-8", errors="replace"),
        )

        process_webhook_event.delay(str(event.id))
        return Response({"id": str(event.id), "accepted": True}, status=status.HTTP_202_ACCEPTED)


class WebhookEventReplayView(APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def post(_request, event_id):
        event = WebhookEvent.objects.get(id=event_id)
        process_webhook_event.delay(str(event.id))
        return Response({"id": str(event.id), "replayed": True}, status=status.HTTP_202_ACCEPTED)


class WebhookEventListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebhookEventSerializer

    def get_queryset(self):
        integration_id = self.kwargs["integration_id"]
        qs = WebhookEvent.objects.filter(integration_id=integration_id).order_by("-received_at")

        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)

        sig_valid = self.request.query_params.get("signature_valid")
        if sig_valid in ("true", "false"):
            qs = qs.filter(signature_valid=(sig_valid == "true"))

        return qs


class WebhookEventDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WebhookEventDetailSerializer
    queryset = WebhookEvent.objects.all()
    lookup_field = "id"
