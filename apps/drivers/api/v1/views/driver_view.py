from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.drivers.models import Driver
from apps.drivers.api.v1.serializers import DriverRegistrationSerializer, DriverListSerializer, DriverDetailSerializer



@extend_schema_view(
    list=extend_schema(
        tags=["Driver Management"],
        summary="List all drivers",
        description="Retrieve a list of all drivers.",
    ),
    retrieve=extend_schema(
        tags=["Driver Management"],
        summary="Retrieve a driver",
        description="Retrieve a specific driver by ID.",
    ),
    create=extend_schema(
        tags=["Driver Management"],
        request=DriverRegistrationSerializer,
        summary="Create a new driver",
        description="Create a new driver profile.",
    ),
    update=extend_schema(
        tags=["Driver Management"],
        summary="Update a driver",
        description="Update an existing driver profile.",
    ),
    partial_update=extend_schema(
        tags=["Driver Management"],
        summary="Partially update a driver",
        description="Partially update an existing driver profile.",
    ),
    destroy=extend_schema(
        tags=["Driver Management"],
        summary="Delete a driver",
        description="Delete an existing driver profile.",
    ),
)
class DriverViewSet(ModelViewSet):
    """
    ViewSet for the Driver model.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """
        Optionally restricts the returned drivers to a given user,
        by filtering against a `user` query parameter in the URL.
        """
        queryset = self.queryset
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        return queryset
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return DriverRegistrationSerializer
        elif self.action == 'retrieve':
            return DriverDetailSerializer
        return DriverListSerializer