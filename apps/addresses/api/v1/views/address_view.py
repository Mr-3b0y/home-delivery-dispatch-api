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
        
