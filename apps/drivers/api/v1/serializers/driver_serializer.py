from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.drivers.models import Driver
from apps.users.models import User


class DriverRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Driver model during registration.
    """
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False,
                                       help_text=_("Optional. Provide the ID of an existing User to convert them into a Driver. If provided, user-related fields (username, email, password, etc.) are ignored."))

    class Meta:
        model = Driver
        fields = ('username', 'email', 'password', 'password2', 'first_name',
                  'last_name', 'phone_number', 'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_color',
                  'current_latitude', 'current_longitude', 'is_available', 'user_id')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'vehicle_plate': {'required': True},
            'vehicle_model': {'required': True},
            'vehicle_year': {'required': True},
            'vehicle_color': {'required': True},
            'current_latitude': {'required': True},
            'current_longitude': {'required': True},
        }
        
    def validate(self, attrs):
        """
        Validate the input data.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
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
                current_latitude = validated_data['current_latitude'],
                current_longitude = validated_data['current_longitude'],
                is_available = validated_data['is_available'])
            driver.save()
            return driver
        
        validated_data.pop('password2')
        driver = Driver.objects.create_user(**validated_data)
        driver.vehicle_plate = validated_data['vehicle_plate']
        driver.vehicle_model = validated_data['vehicle_model']
        driver.vehicle_year = validated_data['vehicle_year']
        driver.vehicle_color = validated_data['vehicle_color']
        driver.current_latitude = validated_data['current_latitude']
        driver.current_longitude = validated_data['current_longitude']
        driver.is_available = validated_data.get('is_available', True)
        driver.save()
        return driver

class DriverListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing the Driver model.
    """
    class Meta:
        model = Driver
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_color')
        read_only_fields = ('id',)

class DriverDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the Driver model.
    """
    class Meta:
        model = Driver
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        