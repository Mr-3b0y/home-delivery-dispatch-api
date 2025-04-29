from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.addresses.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address model.
    """
    
    coordinates = GeometryField(
        help_text=_("Coordinates of the address."),
    )
    
    class Meta:
        model = Address
        fields = ('id', 'street', 'city', 'state', 'country', 'postal_code',
                  'coordinates','reference', 'created_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
        extra_kwargs = {
            'city': {'required': True},
            'state': {'required': True},
            'country': {'required': True},
            'postal_code': {'required': True},
            'coordinates': {'required': True},
            # 'latitude': {'required': True},
            # 'longitude': {'required': True},
        }
            
    def validate(self, data):
        """
        Validate latitude and longitude coordinates.
        """
        # Add coordinate validation logic here if needed
        return data
