from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema
from django_filters.rest_framework import DjangoFilterBackend

from apps.drivers.models import Driver
from apps.drivers.api.v1.serializers import DriverRegistrationSerializer, DriverListSerializer, DriverDetailSerializer
from apps.drivers.permissions import IsAdminOrSelf


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
    
    Permissions:
    - Admin users can perform any action (list, create, retrieve, update, delete)
    - Drivers can only retrieve and update their own information
    - Only admins can list all drivers
    """
    queryset = Driver.objects.all().order_by('-date_joined')
    serializer_class = DriverListSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_available', 'vehicle_model', 'vehicle_year', 'vehicle_color', 'id', 'username', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return DriverRegistrationSerializer
        elif self.action == 'retrieve':
            return DriverDetailSerializer
        return DriverListSerializer