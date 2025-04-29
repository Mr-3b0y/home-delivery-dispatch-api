from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from apps.drivers.models import Driver
from apps.users.models import User


class DriverRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Driver model during registration.
    """
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    user_id = serializers.IntegerField(write_only=True, required=False,
                                       help_text=_("Optional. Provide the ID of an existing User to convert them into a Driver. If provided, user-related fields (username, email, password, etc.) are ignored."))

    location_coordinates = GeometryField(
        help_text=_("Coordinates of the driver's location."),
    )
    
    class Meta:
        model = Driver
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name',
                  'last_name', 'phone_number', 'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_color',
                   'is_available', 'location_coordinates','user_id')
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'vehicle_plate': {'required': True},
            'vehicle_model': {'required': True},
            'vehicle_year': {'required': True},
            'vehicle_color': {'required': True},
            'location_coordinates': {'required': True},
            
        }
        
    def validate_location_coordinates(self, value):
        """
        Validate that location_coordinates contains valid geographic coordinates.
        """
        if value is None:
            raise serializers.ValidationError("Location coordinates are required.")
        if hasattr(value, 'x') and hasattr(value, 'y'):
            # Longitude (x) must be between -180 and 180
            if not (-180 <= value.x <= 180):
                raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
                
            # Latitude (y) must be between -90 and 90
            if not (-90 <= value.y <= 90):
                raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
                
        return value
        
    def validate(self, attrs):
        """
        Validate the input data.
        """
        # Only validate passwords if both are provided (for create or password change)
        if 'password' in attrs and 'password2' in attrs:
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError("Passwords do not match.")
        # If only one password field is provided, raise error
        elif 'password' in attrs or 'password2' in attrs:
            raise serializers.ValidationError("Both password fields must be provided.")
        
        return attrs
        
    def create(self, validated_data):
        """
        Create a new driver instance.
        """
        if validated_data.get('user_id'):
            user = User.objects.get(id=validated_data['user_id'])
            if not user:
                raise ValidationError(_(f"User {validated_data['user_id']} not found."))
            driver = Driver.objects.create(
                user_ptr_id=user.id,
                vehicle_plate = validated_data['vehicle_plate'],
                vehicle_model = validated_data['vehicle_model'],
                vehicle_year = validated_data['vehicle_year'],
                vehicle_color = validated_data['vehicle_color'],
                location_coordinates = validated_data['location_coordinates'],
                is_available = validated_data['is_available'])
            driver.save()
            return driver
        
        if 'password2' in validated_data:
            validated_data.pop('password2')
            
        driver = Driver.objects.create_user(**validated_data)
        driver.save()
        return driver
        
    def update(self, instance, validated_data):
        """
        Update a driver instance.
        """
        # Handle password update if provided
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
            
        # Remove password2 field which is not needed for update
        if 'password2' in validated_data:
            validated_data.pop('password2')
            
        # Update the rest of the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance

class DriverListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing the Driver model.
    """
    
    location_coordinates = GeometryField(
        help_text=_("Coordinates of the driver's location."),
    )
    
    class Meta:
        model = Driver
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
                  'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_color', 'is_available', 'location_coordinates')
        read_only_fields = ('id',)


class DriverDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Driver model.
    """
    
    location_coordinates = GeometryField(
        help_text=_("Coordinates of the driver's location."),
    )
    
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
