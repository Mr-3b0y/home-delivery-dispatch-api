from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter



@extend_schema_view(
    post=extend_schema(
        tags=["Authentication JWT"],
        summary="Refresh JWT token",
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view to refresh JWT token.
    """
    pass
