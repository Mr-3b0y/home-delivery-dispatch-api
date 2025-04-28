from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.services.models import Service
from apps.drivers.api.v1.serializers import DriverListSerializer
from apps.users.api.v1.serializers import UserSerializer


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """
    
    driver = DriverListSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    
    class Meta:
        model = Service
        fields = ('id', 'pickup_address', 'distance_km', 'estimated_arrival_minutes',
                  'driver', 'status', 'client')
        read_only_fields = ['id', 'created_at', 'updated_at', 'driver', 'status', 'client',
                            'distance_km', 'estimated_arrival_minutes']
    
    def validate_pickup_address(self, value):
        """
        Validate that the pickup address belongs to the user creating the service.
        """
        request = self.context.get('request')
        if request and request.user:
            if value.created_by != request.user:
                raise ValidationError(_("You can only use addresses that belong to you."))
        return value