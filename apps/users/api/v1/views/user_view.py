from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from apps.users.api.v1.serializers import UserSerializer, UserDetailSerializer
from apps.users.models import User


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