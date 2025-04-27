from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from apps.users.api.v1.serializers import UserSerializer, UserDetailSerializer
from apps.users.models import User


@extend_schema_view(
    list=extend_schema(
        tags=["User Management"],
        summary="Get user list",
    ),
    retrieve=extend_schema(
        tags=["User Management"],
        summary="Get user detail",
    ),
    create=extend_schema(
        tags=["User Management"],
        summary="Create a new user",
    ),
    update=extend_schema(
        tags=["User Management"],
        summary="Update a user",
    ),
    partial_update=extend_schema(
        tags=["User Management"],
        summary="Partial update a user",
    ),
    destroy=extend_schema(
        tags=["User Management"],
        summary="Delete a user",
    ),
)
class UserViewSet(ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    # lookup_field = 'username'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return super().get_serializer_class()