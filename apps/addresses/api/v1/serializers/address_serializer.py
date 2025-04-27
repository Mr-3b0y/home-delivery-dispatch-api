from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.addresses.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address model.
    """
    class Meta:
        model = Address
        fields = ('id', 'street', 'city', 'state', 'country', 'postal_code', 'latitude', 'longitude', 'reference', 'created_by')
        read_only_fields = ('id', 'created_by')
        extra_kwargs = {
            'city': {'required': True},
            'state': {'required': True},
            'country': {'required': True},
            'postal_code': {'required': True},
            'latitude': {'required': True},
            'longitude': {'required': True},
            }
            
        def validate(self, data):
            """
            Validate latitude and longitude coordinates.
            """
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if latitude is not None and (latitude < -90 or latitude > 90):
                raise ValidationError(_("Latitude must be between -90 and 90 degrees."))
            
            if longitude is not None and (longitude < -180 or longitude > 180):
                raise ValidationError(_("Longitude must be between -180 and 180 degrees."))
            
            return data
        
    
    