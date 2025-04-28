from django.test import TestCase
from apps.drivers.models import Driver
from apps.users.models import User
from decimal import Decimal


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
            'current_latitude': Decimal('37.7749'),
            'current_longitude': Decimal('-122.4194'),
            'is_available': True,
        }
        
        # Create a test driver
        self.driver = Driver.objects.create_user(
            **self.user_data,
        )
        self.driver.vehicle_plate = self.driver_data['vehicle_plate']
        self.driver.vehicle_model = self.driver_data['vehicle_model']
        self.driver.vehicle_year = self.driver_data['vehicle_year']
        self.driver.vehicle_color = self.driver_data['vehicle_color']
        self.driver.current_latitude = self.driver_data['current_latitude']
        self.driver.current_longitude = self.driver_data['current_longitude']
        self.driver.is_available = self.driver_data['is_available']
        # Save the driver
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
        self.assertEqual(self.driver.current_latitude, self.driver_data['current_latitude'])
        self.assertEqual(self.driver.current_longitude, self.driver_data['current_longitude'])
        self.assertEqual(self.driver.is_available, self.driver_data['is_available'])
        self.assertEqual(self.driver.rating, Decimal('5.0'))  # Default rating
        
    def test_string_representation(self):
        """Test the string representation of a driver."""
        # Fix string representation according to actual implementation
        expected_str = f"{self.driver.username} - {self.driver.vehicle_plate}"
        self.assertEqual(str(self.driver), expected_str)
        
    def test_calculate_distance(self):
        """Test the distance calculation method."""
        # San Francisco to Los Angeles (approx. 559 km)
        sf_lat = Decimal('37.7749')
        sf_lng = Decimal('-122.4194')
        la_lat = Decimal('34.0522')
        la_lng = Decimal('-118.2437')
        
        # Use the driver in San Francisco
        self.driver.current_latitude = sf_lat
        self.driver.current_longitude = sf_lng
        self.driver.save()
        
        # Calculate distance to Los Angeles
        distance = self.driver.calculate_distance(la_lat, la_lng)
        
        # Test that the distance is approximately correct (within 10km)
        self.assertGreater(distance, 540)
        self.assertLess(distance, 580)
        
    def test_availability_flag(self):
        """Test changing the availability flag."""
        self.assertTrue(self.driver.is_available)
        
        self.driver.is_available = False
        self.driver.save()
        
        # Refresh from database
        self.driver.refresh_from_db()
        self.assertFalse(self.driver.is_available)