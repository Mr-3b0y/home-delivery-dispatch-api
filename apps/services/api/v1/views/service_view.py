from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse

from apps.services.models import Service
from apps.services.api.v1.serializers import ServiceSerializer, ServiceCancelSerializer
from apps.drivers.models import Driver
from apps.services.utils import get_closest_driver, get_arrival_time


@extend_schema_view(
    list=extend_schema(
        tags=["Service"],
        summary="List all services",
        description="Retrieve a list of all services.",
    ),
    retrieve=extend_schema(
        tags=["Service"],
        summary="Retrieve a service",
        description="Retrieve a specific service by ID.",
    ),
    create=extend_schema(
        tags=["Service"],
        summary="Create a new service",
        description="Create a new service with the provided data.",
    ),
    update=extend_schema(
        tags=["Service"],
        summary="Update a service",
        description="Update an existing service with the provided data.",
    ),
    partial_update=extend_schema(
        tags=["Service"],
        summary="Partially update a service",
        description="Partially update an existing service with the provided data.",
    ),
    destroy=extend_schema(
        tags=["Service"],
        summary="Delete a service",
        description="Delete a specific service by ID.",
    ),
)
class ServiceViewSet(ModelViewSet):
    """
    ViewSet for the Service model.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        drivers_availables = Driver.objects.filter(is_available=True)
        pickup_address = serializer.validated_data.get('pickup_address')
        if not drivers_availables.exists():
            return Response({"detail": "No available drivers."}, status=status.HTTP_400_BAD_REQUEST)
        
        closest_driver, closest_distance = get_closest_driver(drivers_availables, pickup_address)
        estimated_arrival_minutes = get_arrival_time(closest_distance)
        
        serializer.save(driver=closest_driver,
                        distance_km=closest_distance,
                        estimated_arrival_minutes=estimated_arrival_minutes,
                        status=Service.STATUS_CHOICES[1][1])
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @extend_schema(
        tags=["Service"],
        summary="Update status of a service to in progress",
        description="Mark a service as in progress.",
    )
    @action(detail=True, methods=['patch'], url_path='in-progress')
    def in_progress(self, request, pk=None):
        """
        Mark a service as in progress.
        """
        if self.request.user.id != self.get_object().driver.id:
            return Response({"detail": "You do not have permission to update this service."}, status=status.HTTP_403_FORBIDDEN)
        
        service = self.get_object()
        if service.status != 'ASSIGNED':
            return Response({"detail": "Service is not assigned."}, status=status.HTTP_400_BAD_REQUEST)
        
        service.status = Service.STATUS_CHOICES[2][1]
        service.save()
        
        serializer = self.get_serializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(
        tags=["Service"],
        summary="Update status of a service to completed",
        description="Mark a service as completed.",
    )
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """
        Mark a service as completed.
        """
        if self.request.user.id != self.get_object().driver.id:
            return Response({"detail": "You do not have permission to complete this service."}, status=status.HTTP_403_FORBIDDEN)
        
        service = self.get_object()
        if service.status != 'IN_PROGRESS':
            return Response({"detail": "Service is not in progress."}, status=status.HTTP_400_BAD_REQUEST)
        
        service.status = Service.STATUS_CHOICES[3][1]
        service.save()
        
        serializer = self.get_serializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @extend_schema(
        tags=["Service"],
        summary="Cancel a service",
        description="Cancel a service with a reason.",
        request=ServiceCancelSerializer,
        responses={
            200: ServiceSerializer,
        },
    )
    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        """
        Cancel a service.
        """
        if self.request.user.id != self.get_object().client.id or self.request.user.id != self.get_object().driver.id:
            return Response({"detail": "You do not have permission to cancel this service."}, status=status.HTTP_403_FORBIDDEN)
        
        service = self.get_object()
        if service.status == 'CANCELLED':
            return Response({"detail": "Service is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)
        
        cancellation_reason = request.data.get('cancellation_reason')
        serializer = ServiceCancelSerializer(data=request.data, instance=service)
        serializer.is_valid(raise_exception=True)
        service.status = Service.STATUS_CHOICES[4][1]
        service.cancellation_reason = cancellation_reason
        service.save()
        
        serializer = self.get_serializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)