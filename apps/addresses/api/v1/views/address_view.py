from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from apps.addresses.models import Address
from apps.addresses.api.v1.serializers import AddressSerializer
from apps.addresses.permissions import IsOwnerOrAdmin


@extend_schema_view(
    list=extend_schema(
        tags=["Address Management"],
        summary="List all addresses",
        description="Retrieve a list of all addresses.",
    ),
    retrieve=extend_schema(
        tags=["Address Management"],
        summary="Retrieve an address",
        description="Retrieve a specific address by ID.",
    ),
    create=extend_schema(
        tags=["Address Management"],
        request=AddressSerializer,
        summary="Create a new address",
        description="Create a new address profile.",
    ),
    update=extend_schema(
        tags=["Address Management"],
        summary="Update an address",
        description="Update an existing address profile.",
    ),
    partial_update=extend_schema(
        tags=["Address Management"],
        summary="Partially update an address",
        description="Partially update an existing address profile.",
    ),
    destroy=extend_schema(
        tags=["Address Management"],
        summary="Delete an address",
        description="Delete an existing address profile.",
    ),
)
class AddressViewSet(ModelViewSet):
    """
    ViewSet for the Address model.
    
    This ViewSet provides all CRUD operations for addresses.
    Regular users can only see and modify their own addresses.
    Admin users can see and modify all addresses.
    """
    queryset = Address.objects.all().order_by('id')
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Optionally restricts the returned addresses to a given user,
        by filtering against a `user` query parameter in the URL or 
        limiting to the user's own addresses.
        """
        queryset = self.queryset
        if self.request.user.is_superuser or self.request.user.is_staff:
            # Admin can see all addresses
            return queryset
        # Regular users can only see their own addresses
        return queryset.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """
        Save the address with the current user as the creator.
        """
        serializer.save(created_by=self.request.user)
        
    @extend_schema(
        parameters=[
            OpenApiParameter(name='latitude', description='Latitude of the center point', required=True, type=float),
            OpenApiParameter(name='longitude', description='Longitude of the center point', required=True, type=float),
            OpenApiParameter(name='distance_km', description='Maximum distance in kilometers', required=False, type=float, default=10.0),
        ],
        tags=["Address Management"],
        summary="Find nearby addresses",
        description="Find addresses within a specified distance from a given latitude and longitude.",
    )
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Find addresses near a given location.
        
        Query Parameters:
            latitude (float): Latitude of the center point
            longitude (float): Longitude of the center point
            distance_km (float): Maximum distance in kilometers (default: 10.0)
        """
        try:
            latitude = request.query_params.get('latitude')
            longitude = request.query_params.get('longitude')
            max_distance = request.query_params.get('distance_km', 10.0)
            
            if not latitude or not longitude:
                return Response(
                    {'error': 'Latitude and longitude parameters are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Create a temporary reference point
            reference_point = Address(
                latitude=Decimal(latitude),
                longitude=Decimal(longitude),
                # Other required fields with placeholder values
                street="",
                city="",
                state="",
                country="",
                postal_code=""
            )
            
            # Get all addresses from the queryset
            queryset = self.get_queryset()
            nearby_addresses = []
            
            # Filter addresses by calculated distance
            for address in queryset:
                distance = address.calculate_distance(reference_point)
                if distance <= float(max_distance):
                    # Add distance to the address data
                    address_data = self.get_serializer(address).data
                    address_data['distance_km'] = round(distance, 2)
                    nearby_addresses.append(address_data)
                    
            # Sort by distance
            nearby_addresses.sort(key=lambda x: x['distance_km'])
            
            return Response(nearby_addresses)
            
        except ValueError:
            return Response(
                {'error': 'Invalid latitude or longitude values'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
