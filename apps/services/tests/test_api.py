from decimal import Decimal
from unittest import mock
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.services.models import Service
from apps.users.models import User
from apps.drivers.models import Driver
from apps.addresses.models import Address


class ServiceAPITestCase(APITestCase):
    """Test case for the Service API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            username='api_admin',
            email='api_admin@example.com',
            password='testpassword123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            phone_number='+34622345674'
        )
        
        self.client_user = User.objects.create_user(
            username='api_client',
            email='api_client@example.com',
            password='testpassword123',
            first_name='Client',
            last_name='User',
            phone_number='+34622345675'
        )
        
        self.driver_user = User.objects.create_user(
            username='api_driver',
            email='api_driver@example.com',
            password='testpassword123',
            first_name='Driver',
            last_name='User',
            phone_number='+34622345676'
        )
        
        # Create a driver correctamente copiando los campos del usuario
        self.driver = Driver(
            user_ptr_id=self.driver_user.id,
            username=self.driver_user.username,
            email=self.driver_user.email,
            password=self.driver_user.password,
            first_name=self.driver_user.first_name,
            last_name=self.driver_user.last_name,
            phone_number=self.driver_user.phone_number,
            is_staff=self.driver_user.is_staff,
            is_active=self.driver_user.is_active,
            date_joined=self.driver_user.date_joined,
            vehicle_plate='XYZ987',
            vehicle_model='Tesla Model 3',
            vehicle_year=2023,
            vehicle_color='Silver',
            current_latitude=40.7128,
            current_longitude=-74.0060,
            is_available=True
        )
        self.driver.save()
        
        # Create addresses
        self.client_address = Address.objects.create(
            street='Test Street',
            state='Test State',
            city='Client City',
            country='Client Country',
            latitude=40.7128,
            longitude=-74.0060,
            created_by=self.client_user
        )
        
        self.other_user_address = Address.objects.create(
            street='Test Street',
            state='Test State',
            city='Other City',
            country='Other Country',
            latitude=34.0522,
            longitude=-118.2437,
            created_by=self.admin_user
        )
        
        # Create services
        self.client_service = Service.objects.create(
            client=self.client_user,
            driver=self.driver,
            pickup_address=self.client_address,
            status='IN_PROGRESS',
            distance_km=Decimal('5.5'),
            estimated_arrival_minutes=10
        )
        
        # API client
        self.client = APIClient()
        
        # URLs - Update with namespace
        self.list_url = reverse('urls-v1:service-list')
        self.detail_url = reverse('urls-v1:service-detail', kwargs={'pk': self.client_service.pk})
        self.complete_url = reverse('urls-v1:service-complete', kwargs={'pk': self.client_service.pk})

    def test_list_services_as_admin(self):
        """Test that admin can see all services."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), Service.objects.count())

    def test_list_services_as_client(self):
        """Test that client can only see their own services."""
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), Service.objects.filter(client=self.client_user).count())
        

    def test_list_services_as_driver(self):
        """Test that driver can only see services assigned to them."""
        self.client.force_authenticate(user=self.driver_user)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), Service.objects.filter(driver=self.driver).count())
        

    def test_retrieve_service_as_client(self):
        """Test that client can retrieve their own service."""
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.client_service.id)

    def test_create_service_with_available_drivers(self):
        """Test creating a service when drivers are available."""
        self.client.force_authenticate(user=self.client_user)
        
        # Mock the utility functions
        with mock.patch('apps.services.api.v1.views.service_view.get_closest_driver') as mock_get_driver, \
             mock.patch('apps.services.api.v1.views.service_view.get_arrival_time') as mock_get_time:
            
            mock_get_driver.return_value = (self.driver, Decimal('3.5'))
            mock_get_time.return_value = 7
            
            data = {
                'pickup_address': self.client_address.id
            }
            
            response = self.client.post(
                self.list_url,
                data,
                format='json'
            )
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['client']['id'], self.client_user.id)
            self.assertEqual(response.data['driver']['id'], self.driver.id)
            self.assertEqual(response.data['pickup_address'], self.client_address.id)
            self.assertEqual(response.data['status'], 'IN_PROGRESS')
            self.assertEqual(Decimal(response.data['distance_km']), Decimal('3.5'))
            self.assertEqual(response.data['estimated_arrival_minutes'], 7)

    def test_create_service_with_no_available_drivers(self):
        """Test creating a service when no drivers are available."""
        self.client.force_authenticate(user=self.client_user)
        
        # Set all drivers as unavailable
        Driver.objects.update(is_available=False)
        
        data = {
            'pickup_address': self.client_address.id
        }
        
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No drivers are currently available', response.data['detail'])

    def test_create_service_with_invalid_address(self):
        """Test creating a service with an address that doesn't belong to the user."""
        self.client.force_authenticate(user=self.client_user)
        
        data = {
            'pickup_address': self.other_user_address.id
        }
        
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You can only use addresses that belong to you', str(response.data))

    def test_complete_service(self):
        """Test marking a service as completed."""
        self.client.force_authenticate(user=self.driver_user)
        
        
        # Service is initially IN_PROGRESS
        self.assertEqual(self.client_service.status, 'IN_PROGRESS')
        
        response = self.client.patch(self.complete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        # Refresh the service from database
        self.client_service.refresh_from_db()
        self.driver.refresh_from_db()
        
        # Check that service status is updated and driver is available
        self.assertEqual(self.client_service.status, 'COMPLETED')
        self.assertTrue(self.driver.is_available)

    def test_complete_already_completed_service(self):
        """Test marking an already completed service as completed."""
        self.client.force_authenticate(user=self.driver_user)
        
        # Set service as COMPLETED
        self.client_service.status = 'COMPLETED'
        self.client_service.save()
        
        response = self.client.patch(self.complete_url)
        
        # Should return bad request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Service is not in progress', response.data['detail'])

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the API."""
        # Try to list services
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Try to retrieve a service
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Try to create a service
        data = {
            'pickup_address': self.client_address.id
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Try to complete a service
        response = self.client.patch(self.complete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)