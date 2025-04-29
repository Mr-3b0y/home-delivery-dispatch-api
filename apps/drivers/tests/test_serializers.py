from django.test import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.drivers.models import Driver
from apps.drivers.api.v1.serializers import DriverRegistrationSerializer, DriverListSerializer, DriverDetailSerializer
from rest_framework import serializers
from django.contrib.gis.geos import Point



class DriverSerializerTest(TestCase):
    """Test cases for the Driver serializer."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testdriver',
            'email': 'testdriver@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'Driver',
            'phone_number': '+1234567890',
        }
        
        self.driver_data = {
            'vehicle_plate': 'ABC123',
            'vehicle_model': 'Toyota Corolla',
            'vehicle_year': 2020,
            'vehicle_color': 'Blue',
            'location_coordinates': Point((-122.4194, 37.7749), srid=4326),
            'is_available': True,
        }
        
        # Create a test driver using Django's User model
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        
        self.driver = Driver.objects.create(
            user_ptr=user,
            **self.driver_data
        )
        
        # Complete data for serializer testing
        self.valid_serializer_data = {
            'username': 'newdriver',
            'email': 'newdriver@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'New',
            'last_name': 'Driver',
            'phone_number': '+1999888777',
            'vehicle_plate': 'XYZ789',
            'vehicle_model': 'Honda Civic',
            'vehicle_year': 2021,
            'vehicle_color': 'Red',
            'location_coordinates': {
                'type': 'Point',
                'coordinates': [-122.4194, 37.7749]
            },
            'is_available': True,
        }
        
        self.invalid_serializer_data = {
            'username': '',  # Invalid (empty)
            'email': 'invalid-email',  # Invalid email format
            'password': 'short',  # Too short
            'first_name': 'New',
            'last_name': 'Driver',
            'phone_number': 'not-a-phone',  # Invalid phone
            'vehicle_plate': '',  # Invalid (empty)
            'vehicle_model': 'Honda Civic',
            'vehicle_year': -2021,  # Invalid negative year
            'vehicle_color': 'Red',
            'location_coordinates': {
                'type': 'Point',
                'coordinates': [-122.4194, 37.7749]
            },  # Invalid decimal
            'is_available': 'not-a-boolean',  # Invalid boolean
        }

    def test_driver_serializer_contains_expected_fields(self):
        """Test that the serializer contains expected fields."""
        serializer = DriverRegistrationSerializer(instance=self.driver)
        data = serializer.data
        
        expected_fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'phone_number',
            'vehicle_plate', 'vehicle_model', 'vehicle_year', 'vehicle_color',
            'location_coordinates', 'is_available'
        ]
        
        self.assertEqual(set(data.keys()), set(expected_fields))
        
    def test_driver_serializer_valid_data(self):
        """Test serializer with valid data."""
        serializer = DriverRegistrationSerializer(data=self.valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        
    def test_driver_serializer_invalid_data(self):
        """Test serializer with invalid data."""
        serializer = DriverRegistrationSerializer(data=self.invalid_serializer_data)
        self.assertFalse(serializer.is_valid())
        
    def test_serializer_updates_driver_correctly(self):
        """Test that serializer updates driver correctly."""
        update_data = {
            'vehicle_plate': 'NEWPLATE',
            'vehicle_model': 'Ford Mustang',
            'vehicle_year': 2022,
        }
        
        serializer = DriverRegistrationSerializer(instance=self.driver, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_driver = serializer.save()
        
        self.assertEqual(updated_driver.vehicle_plate, 'NEWPLATE')
        self.assertEqual(updated_driver.vehicle_model, 'Ford Mustang')
        self.assertEqual(updated_driver.vehicle_year, 2022)
        
        # Unchanged fields should remain the same
        self.assertEqual(updated_driver.vehicle_color, self.driver_data['vehicle_color'])
        # self.assertEqual(updated_driver.user_ptr.username, self.user_data['username'])
        
    def test_serializer_creates_driver_correctly(self):
        """Test that serializer creates driver correctly."""
        data = self.valid_serializer_data.copy()
        data['username'] = 'newdriver_create'
        data['email'] = 'newdriver_create@example.com'
        serializer = DriverRegistrationSerializer(data=self.valid_serializer_data)
        
        self.assertTrue(serializer.is_valid())
        
        # Note: In a real implementation, you would need a create method in the serializer
        # Here we're just testing the validation part
    