from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.drivers.models import Driver
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal


class DriverAPITestCase(APITestCase):
    """Test cases for the Driver API."""

    def setUp(self):
        """Set up test data."""
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword123',
            phone_number='+1987654321',
            is_staff=True,
            is_superuser=True
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='userpassword123',
            phone_number='+1234567890',
        )
        
        # Create driver data
        self.driver_data = {
            'username': 'testdriver',
            'email': 'testdriver@example.com',
            'password': 'driverpassword123',
            'first_name': 'Test',
            'last_name': 'Driver',
            'phone_number': '+1555123456',
            'vehicle_plate': 'ABC123',
            'vehicle_model': 'Toyota Corolla',
            'vehicle_year': 2020,
            'vehicle_color': 'Blue',
            'current_latitude': Decimal('37.7749'),
            'current_longitude': Decimal('-122.4194'),
            'is_available': True,
        }
        
        # Create test driver in a simpler way but handling all required fields
        # 1. Create a User object with the user fields
        user_fields = {
            'username': self.driver_data['username'],
            'email': self.driver_data['email'],
            'password': self.driver_data['password'],
            'first_name': self.driver_data['first_name'],
            'last_name': self.driver_data['last_name'],
            'phone_number': self.driver_data['phone_number']
        }
        
        # Use create_user for the User part
        user = User.objects.create_user(**user_fields)
        
        # 2. Create the Driver with explicitly provided fields, including all required ones
        self.driver = Driver(
            user_ptr_id=user.id,  # Use the same ID as the user
            username=user.username,
            password=user.password,  # Already hashed by create_user
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            is_staff=user.is_staff,
            is_active=user.is_active,
            date_joined=user.date_joined,
            # Driver-specific fields
            vehicle_plate=self.driver_data['vehicle_plate'],
            vehicle_model=self.driver_data['vehicle_model'],
            vehicle_year=self.driver_data['vehicle_year'],
            vehicle_color=self.driver_data['vehicle_color'],
            current_latitude=self.driver_data['current_latitude'],
            current_longitude=self.driver_data['current_longitude'],
            is_available=self.driver_data['is_available']
        )
        
        # 3. Save the driver object
        self.driver.save()
        
        # Refresh from database to ensure all fields are properly set
        self.driver.refresh_from_db()
        
        # Generate tokens
        self.admin_token = str(RefreshToken.for_user(self.admin).access_token)
        self.user_token = str(RefreshToken.for_user(self.user).access_token)
        self.driver_token = str(RefreshToken.for_user(self.driver).access_token)
        
        # URL endpoints with namespace
        self.list_create_url = reverse('urls-v1:driver-list')
        self.detail_url = reverse('urls-v1:driver-detail', args=[self.driver.id])
    
    # Helper method for creating a driver in tests
    def create_test_driver(self, username, **kwargs):
        """Helper to create a test driver with all required fields."""
        # Create a user first
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='password123',
            phone_number=f'+1{username[-1]}222333444',
            first_name=f'Test{username[-1]}',
            last_name='Driver'
        )
        
        # Create driver fields
        driver = Driver(
            user_ptr_id=user.id,  # Use the same ID as the user
            # Driver-specific fields with defaults
            vehicle_plate=kwargs.get('vehicle_plate', f'PLATE-{username}'),
            vehicle_model=kwargs.get('vehicle_model', 'Toyota Corolla'),
            vehicle_year=kwargs.get('vehicle_year', 2020),
            vehicle_color=kwargs.get('vehicle_color', 'Blue'),
            current_latitude=kwargs.get('current_latitude', Decimal('37.7749')),
            current_longitude=kwargs.get('current_longitude', Decimal('-122.4194')),
            is_available=kwargs.get('is_available', True)
        )
        
        # Save directly
        driver.save()
        
        return Driver.objects.get(id=user.id)
        
    def get_auth_header(self, token):
        """Return the Authorization header with the given token."""
        return {'Authorization': f'Bearer {token}'}
        
    def test_list_drivers_as_admin(self):
        """Test that admin can list all drivers."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
    def test_list_drivers_as_regular_user(self):
        """Test that regular users cannot list drivers."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get(self.list_create_url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_retrieve_driver_as_admin(self):
        """Test that admin can retrieve a driver."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.driver_data['username'])
        self.assertEqual(response.data['email'], self.driver_data['email'])
        self.assertEqual(response.data['vehicle_plate'], self.driver_data['vehicle_plate'])
        
    def test_create_driver(self):
        """Test driver creation through API."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        new_driver_data = {
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
            'current_latitude': '38.9072',
            'current_longitude': '-77.0369',
            'is_available': True,
        }
        
        response = self.client.post(self.list_create_url, new_driver_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify driver was created
        self.assertTrue(Driver.objects.filter(username='newdriver').exists())
        new_driver = Driver.objects.get(username='newdriver')
        self.assertEqual(new_driver.vehicle_plate, 'XYZ789')
        
    def test_update_driver(self):
        """Test updating a driver."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        update_data = {
            'vehicle_plate': 'UPDATED',
            'vehicle_model': 'Tesla Model 3',
            'is_available': False
        }
        
        response = self.client.patch(self.detail_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify driver was updated
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.vehicle_plate, 'UPDATED')
        self.assertEqual(self.driver.vehicle_model, 'Tesla Model 3')
        self.assertFalse(self.driver.is_available)
        
    def test_delete_driver(self):
        """Test deleting a driver."""
        # Create a driver to delete using our helper method
        driver_to_delete = self.create_test_driver('deldriver', vehicle_plate='DEL123')
        
        delete_url = reverse('urls-v1:driver-detail', args=[driver_to_delete.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Driver.objects.filter(username='deldriver').exists())
        
    def test_filter_drivers(self):
        """Test filtering drivers by user ID."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        
        # Create an extra driver using helper method
        extra_driver = self.create_test_driver('extradriver', vehicle_plate='EXTRA1')
        
        # Test filtering by user_id
        response = self.client.get(f"{self.list_create_url}?id={self.driver.id}")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), 1)
        self.assertEqual(response.data['results'][0]['username'], self.driver.username)
        
    def test_unauthorized_access(self):
        """Test that API requires authentication."""
        # No token provided
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)