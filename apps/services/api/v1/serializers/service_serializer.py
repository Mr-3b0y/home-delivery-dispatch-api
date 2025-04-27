from rest_framework import serializers

from apps.services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Service model.
    """
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'driver', 'status']
        
        
class ServiceCancelSerializer(serializers.ModelSerializer):
    """
    Serializer for canceling a service.
    """
    cancellation_reason = serializers.CharField(required=True)

    class Meta:
        model = Service
        fields = ['cancellation_reason']