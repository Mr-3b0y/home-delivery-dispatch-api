from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication JWT"],
        summary="Verify JWT token",)
)
class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom view to verify JWT token.
    """
    pass
        

                
                