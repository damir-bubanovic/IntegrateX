from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.users.permissions import IsAdmin
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.select_related("actor", "organization").all()
    filter_backends = (DjangoFilterBackend,)

    # Built-in filters
    filterset_fields = ("action", "method", "status_code", "organization", "actor")
