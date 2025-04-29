from django.test import TestCase
from apps.drivers.models import Driver
from apps.users.models import User
from decimal import Decimal
from django.contrib.gis.geos import Point


class DriverModelTest(TestCase):
    """Test cases for the Driver model."""

    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testdrivermodel',
            'email': 'testdrivermodel@example.com',
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
        
        
        # Create a test driver using multi-table inheritance properly
        self.driver = Driver.objects.create(
            username=self.user_data['username'],
            email=self.user_data['email'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            phone_number=self.user_data['phone_number'],
            vehicle_plate=self.driver_data['vehicle_plate'],
            vehicle_model=self.driver_data['vehicle_model'],
            vehicle_year=self.driver_data['vehicle_year'],
            vehicle_color=self.driver_data['vehicle_color'],
            location_coordinates=self.driver_data['location_coordinates'],
            is_available=self.driver_data['is_available']
        )
        self.driver.set_password(self.user_data['password'])
        self.driver.save()
        
        self.driver.refresh_from_db()
        
        
    def test_driver_creation(self):
        """Test that a driver can be created with the expected attributes."""
        
        self.assertEqual(self.driver.username, self.user_data['username'])
        self.assertEqual(self.driver.email, self.user_data['email'])
        self.assertEqual(self.driver.first_name, self.user_data['first_name'])
        self.assertEqual(self.driver.last_name, self.user_data['last_name'])
        self.assertEqual(self.driver.phone_number, self.user_data['phone_number'])
        
        self.assertEqual(self.driver.vehicle_plate, self.driver_data['vehicle_plate'])
        self.assertEqual(self.driver.vehicle_model, self.driver_data['vehicle_model'])
        self.assertEqual(self.driver.vehicle_year, self.driver_data['vehicle_year'])
        self.assertEqual(self.driver.vehicle_color, self.driver_data['vehicle_color'])
        self.assertEqual(self.driver.location_coordinates, self.driver_data['location_coordinates'])
        self.assertEqual(self.driver.is_available, self.driver_data['is_available'])
        
        
        
        
    def test_availability_flag(self):
        """Test changing the availability flag."""
        self.assertTrue(self.driver.is_available)
        
        self.driver.is_available = False
        self.driver.save()
        
        # Refresh from database
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.is_available)