from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from apps.authentication.api.v1.serializers import CustomTokenObtainPairSerializer


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication JWT"],
        summary="Obtain JWT token",
        parameters=[
            OpenApiParameter(
                name="username",
                type=str,
                description="Username of the user",
                required=True,
            ),
            OpenApiParameter(
                name="password",
                type=str,
                description="Password of the user",
                required=True,
            ),
        ],
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token with additional claims.
    """
    
    serializer_class = CustomTokenObtainPairSerializer