from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import HasOrganization, IsOrgMember, IsOrgAdmin


class CurrentOrganizationView(APIView):
    permission_classes = [IsAuthenticated, HasOrganization, IsOrgMember]

    @staticmethod
    def get(request):
        return Response(
            {
                "organization": {
                    "id": request.organization.id,
                    "name": str(request.organization),
                    "slug": request.organization.slug,
                }
            }
        )


class OrgAdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, HasOrganization, IsOrgAdmin]

    @staticmethod
    def get(request):
        return Response(
            {
                "ok": True,
                "org": request.organization.slug,
                "message": "Org admin access granted",
            }
        )
