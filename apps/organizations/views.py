from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CurrentOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not getattr(request, "organization", None):
            return Response({"organization": None})

        return Response({
            "organization": {
                "id": request.organization.id,
                "name": str(request.organization),
                "slug": request.organization.slug,
            }
        })
