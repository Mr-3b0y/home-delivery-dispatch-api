from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from apps.users.api.v1.serializers import UserDetailSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["User Authenticated"],
        summary="Get user profile",
    ),
    put=extend_schema(
        tags=["User Authenticated"],
        summary="Update user profile",
    ),
    patch=extend_schema(
        tags=["User Authenticated"],
        summary="Partial update user profile",
    ),
)
class MeView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update the authenticated user's profile.
    """
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user