from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse

from apps.services.models import Service
from apps.services.api.v1.serializers import ServiceSerializer
from apps.drivers.models import Driver
from apps.services.utils import get_closest_driver, get_arrival_time
from apps.services.persmissions import ServicePermission


@extend_schema_view(
    list=extend_schema(
        tags=["Services"],
        summary="List all services",
        description="Retrieve a list of all services.",
    ),
    retrieve=extend_schema(
        tags=["Services"],
        summary="Retrieve a service",
        description="Retrieve a specific service by ID.",
    ),
    create=extend_schema(
        tags=["Services"],
        summary="Create a new service",
        description="Create a new service with the provided data.",
    ),
    update=extend_schema(
        tags=["Services"],
        summary="Update a service",
        description="Update an existing service with the provided data.",
    ),
    partial_update=extend_schema(
        tags=["Services"],
        summary="Partially update a service",
        description="Partially update an existing service with the provided data.",
    ),
    destroy=extend_schema(
        tags=["Services"],
        summary="Delete a service",
        description="Delete a specific service by ID.",
    ),
)
class ServiceViewSet(ModelViewSet):
    """
    ViewSet for the Service model.
    """
    queryset = Service.objects.all().order_by('-created_at')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, ServicePermission]

    def get_queryset(self):
        """
        Filter services based on the user's role:
        - Admins can see all services
        - Clients can only see their own services
        - Drivers can only see services assigned to them
        """
        user = self.request.user
        queryset = super().get_queryset()
        
        if user.is_staff or user.is_superuser:
            return queryset
            
        client_services = queryset.filter(client=user)
        
        try:
            driver = Driver.objects.get(user_ptr_id=user.id)
            
            driver_services = queryset.filter(driver=driver)
            
            return client_services | driver_services
        except Driver.DoesNotExist:
            return client_services

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        drivers_availables = Driver.objects.filter(is_available=True)
        pickup_address = serializer.validated_data.get('pickup_address')
        if not drivers_availables.exists():
            return Response({
                "detail": "No drivers are currently available to fulfill your service request. Please try again later.",
            }, status=status.HTTP_404_NOT_FOUND)
        
        closest_driver, closest_distance = get_closest_driver(drivers_availables, pickup_address)
        estimated_arrival_minutes = get_arrival_time(closest_distance)
        
        serializer.save(driver=closest_driver,
                        client=self.request.user,
                        distance_km=closest_distance,
                        estimated_arrival_minutes=estimated_arrival_minutes,
                        status='IN_PROGRESS')
        closest_driver.is_available = False
        closest_driver.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    
    
    @extend_schema(
        tags=["Services"],
        summary="Update status of a service to completed",
        description="Mark a service as completed.",
        request=None,
        responses=ServiceSerializer,
    )
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """
        Mark a service as completed by driver.
        """
        service = self.get_object()
        
        if service.status not in ['In progress', 'IN_PROGRESS']:
            return Response({"detail": "Service is not in progress."}, status=status.HTTP_400_BAD_REQUEST)
        
        service.status = 'COMPLETED'
        service.save()
        
        
        driver = service.driver
        driver.is_available = True
        driver.save()
        
        serializer = self.get_serializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)