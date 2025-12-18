from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.organizations.permissions import HasOrganization, IsOrgMember
from .models import Integration
from .providers import get_client
from .serializers import IntegrationSerializer


class IntegrationListCreateView(APIView):
    permission_classes = [IsAuthenticated, HasOrganization, IsOrgMember]

    # noinspection PyMethodMayBeStatic
    def get(self, request):
        qs = Integration.objects.filter(  # type: ignore[attr-defined]
            organization=request.organization
        ).order_by("-id")
        return Response(IntegrationSerializer(qs, many=True).data)

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        serializer = IntegrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        integration = Integration.objects.create(  # type: ignore[attr-defined]
            organization=request.organization,
            **serializer.validated_data,
        )
        return Response(
            IntegrationSerializer(integration).data,
            status=status.HTTP_201_CREATED,
        )


class IntegrationPingView(APIView):
    permission_classes = [IsAuthenticated, HasOrganization, IsOrgMember]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "burst"

    # noinspection PyMethodMayBeStatic
    def post(self, request, integration_id: int):
        integration = (
            Integration.objects.filter(  # type: ignore[attr-defined]
                id=integration_id,
                organization=request.organization,
                is_active=True,
            ).first()
        )
        if not integration:
            raise NotFound("Integration not found")

        client = get_client(
            provider=integration.provider,
            base_url=integration.api_base_url,
            api_key=integration.api_key,
        )

        data = client.ping()
        ok = data.get("ok", True)

        return Response(
            {
                "ok": ok,
                "provider": integration.provider,
                "integration": {"id": integration.pk, "name": integration.name},
                "data": data,
            }
        )
