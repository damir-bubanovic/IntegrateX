from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class OrgContextView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        org = getattr(request, "organization", None)
        return Response({"org": org.slug if org else None})
