from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.authentication.api.v1.serializers import CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication JWT"],
        summary="Obtain JWT token",
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token with additional claims.
    """
    
    serializer_class = CustomTokenObtainPairSerializer