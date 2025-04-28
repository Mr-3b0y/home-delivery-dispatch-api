from unittest import mock
from django.test import TestCase

from apps.services.utils import get_closest_driver, get_arrival_time
from apps.drivers.models import Driver
from apps.addresses.models import Address
from apps.users.models import User


class UtilsTestCase(TestCase):
    """Test case for utility functions in the services app."""

    def setUp(self):
        """Set up test data."""
        # Create driver users
        self.driver_user1 = User.objects.create_user(
            username='utils_driver1',
            email='utils_driver1@example.com',
            password='testpassword123',
            first_name='Driver1',
            last_name='User',
            phone_number='+34612345670'
        )
        
        self.driver_user2 = User.objects.create_user(
            username='utils_driver2',
            email='utils_driver2@example.com',
            password='testpassword123',
            first_name='Driver2',
            last_name='User',
            phone_number='+34612345671'
        )
        
        self.driver_user3 = User.objects.create_user(
            username='utils_driver3',
            email='utils_driver3@example.com',
            password='testpassword123',
            first_name='Driver3',
            last_name='User',
            phone_number='+34612345672'
        )
        
        # Create drivers using la forma correcta, copiando los campos del User existente
        # Driver 1
        self.driver1 = Driver(
            user_ptr_id=self.driver_user1.id,
            username=self.driver_user1.username,
            email=self.driver_user1.email,
            password=self.driver_user1.password,
            first_name=self.driver_user1.first_name,
            last_name=self.driver_user1.last_name,
            phone_number=self.driver_user1.phone_number,
            is_staff=self.driver_user1.is_staff,
            is_active=self.driver_user1.is_active,
            date_joined=self.driver_user1.date_joined,
            vehicle_plate='ABC123',
            vehicle_model='Toyota Camry',
            vehicle_year=2021,
            vehicle_color='Black',
            current_latitude=40.7128,
            current_longitude=-74.0060,
            is_available=True
        )
        self.driver1.save()
        
        # Driver 2
        self.driver2 = Driver(
            user_ptr_id=self.driver_user2.id,
            username=self.driver_user2.username,
            email=self.driver_user2.email,
            password=self.driver_user2.password,
            first_name=self.driver_user2.first_name,
            last_name=self.driver_user2.last_name,
            phone_number=self.driver_user2.phone_number,
            is_staff=self.driver_user2.is_staff,
            is_active=self.driver_user2.is_active,
            date_joined=self.driver_user2.date_joined,
            vehicle_plate='DEF456',
            vehicle_model='Honda Civic',
            vehicle_year=2020,
            vehicle_color='Blue',
            current_latitude=40.7129,
            current_longitude=-74.0061,
            is_available=True
        )
        self.driver2.save()
        
        # Driver 3
        self.driver3 = Driver(
            user_ptr_id=self.driver_user3.id,
            username=self.driver_user3.username,
            email=self.driver_user3.email,
            password=self.driver_user3.password,
            first_name=self.driver_user3.first_name,
            last_name=self.driver_user3.last_name,
            phone_number=self.driver_user3.phone_number,
            is_staff=self.driver_user3.is_staff,
            is_active=self.driver_user3.is_active,
            date_joined=self.driver_user3.date_joined,
            vehicle_plate='GHI789',
            vehicle_model='Ford Focus',
            vehicle_year=2019,
            vehicle_color='Red',
            current_latitude=40.7130,
            current_longitude=-74.0062,
            is_available=True
        )
        self.driver3.save()
        
        # Create a client for the address
        self.client_user = User.objects.create_user(
            username='utils_client',
            email='utils_client@example.com',
            password='testpassword123',
            first_name='Client',
            last_name='User',
            phone_number='+34612345673'
        )
        
        # Create an address
        self.address = Address.objects.create(
            street='Test Street',
            state='Test State',
            city='Test City',
            country='Test Country',
            latitude=40.7128,
            longitude=-74.0060,
            created_by=self.client_user
        )

    def test_get_closest_driver(self):
        """Test finding the closest driver to a given address."""
        # Define a custom side effect for the mock that identifies drivers by their vehicle_plate
        def mock_calculate_distance(self, lat, lon):
            if self.vehicle_plate == 'ABC123':
                return 5.0
            elif self.vehicle_plate == 'DEF456':
                return 2.0
            else:
                return 10.0
        
        # Create patch for the calculate_distance method
        with mock.patch.object(Driver, 'calculate_distance', autospec=True) as mock_calc:
            # Set up our side effect
            mock_calc.side_effect = mock_calculate_distance
            
            # Get available drivers
            drivers = Driver.objects.filter(is_available=True)
            
            # Call the function we're testing
            closest, distance = get_closest_driver(drivers, self.address)
            
            # Driver2 should be closest because we mocked its distance to be 2.0
            self.assertEqual(closest.vehicle_plate, self.driver2.vehicle_plate)
            self.assertEqual(distance, 2.0)

    def test_get_closest_driver_with_no_drivers(self):
        """Test finding the closest driver when no drivers are available."""
        # Delete all drivers
        Driver.objects.all().delete()
        
        drivers = Driver.objects.filter(is_available=True)
        closest, distance = get_closest_driver(drivers, self.address)
        
        # Should return None, inf when no drivers are found
        self.assertIsNone(closest)
        self.assertEqual(distance, float('inf'))

    def test_get_arrival_time(self):
        """Test calculating estimated arrival time based on distance."""
        # Test with different distances
        self.assertEqual(get_arrival_time(60), 60)  # 60 km at 60 km/h = 60 minutes
        self.assertEqual(get_arrival_time(30), 30)  # 30 km at 60 km/h = 30 minutes
        self.assertEqual(get_arrival_time(15), 15)  # 15 km at 60 km/h = 15 minutes
        self.assertEqual(get_arrival_time(7.5), 7.5)  # 7.5 km at 60 km/h = 7.5 minutes
        
        # Test with zero distance
        self.assertEqual(get_arrival_time(0), 0)  # 0 km at 60 km/h = 0 minutes