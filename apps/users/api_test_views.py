from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin


class WhoAmIView(APIView):
    permission_classes = [IsAuthenticated]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get(self, request, *args, **kwargs):
        return Response({
            "id": request.user.id,
            "username": request.user.username,
            "role": request.user.role,
        })


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def get(self, request, *args, **kwargs):
        return Response({
            "ok": True,
            "message": f"You are admin: {request.user.username}",
        })
