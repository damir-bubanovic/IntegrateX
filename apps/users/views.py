from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class IntegrateXTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = getattr(user, "role", "user")
        token["username"] = user.get_username()
        return token


class IntegrateXTokenObtainPairView(TokenObtainPairView):
    serializer_class = IntegrateXTokenObtainPairSerializer
