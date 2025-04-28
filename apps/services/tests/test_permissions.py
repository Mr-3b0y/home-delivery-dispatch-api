from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from apps.services.models import Service
from apps.users.models import User
from apps.drivers.models import Driver
from apps.addresses.models import Address
from apps.services.persmissions import ServicePermission


class ServicePermissionTestCase(TestCase):
    """Test case for the ServicePermission class."""

    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            username='perm_admin',
            email='perm_admin@example.com',
            password='testpassword123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            phone_number='+34632345680'
        )
        
        self.client_user = User.objects.create_user(
            username='perm_client',
            email='perm_client@example.com',
            password='testpassword123',
            first_name='Client',
            last_name='User',
            phone_number='+34632345681'
        )
        
        self.other_client_user = User.objects.create_user(
            username='perm_other_client',
            email='perm_other_client@example.com',
            password='testpassword123',
            first_name='Other',
            last_name='Client',
            phone_number='+34632345682'
        )
        
        self.driver_user = User.objects.create_user(
            username='perm_driver',
            email='perm_driver@example.com',
            password='testpassword123',
            first_name='Driver',
            last_name='User',
            phone_number='+34632345683'
        )
        
        self.other_driver_user = User.objects.create_user(
            username='perm_other_driver',
            email='perm_other_driver@example.com',
            password='testpassword123',
            first_name='Other',
            last_name='Driver',
            phone_number='+34632345684'
        )
        
        # Create drivers correctamente copiando los campos de usuarios existentes
        # Driver principal
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
            vehicle_plate='PERM123',
            vehicle_model='Mercedes Benz',
            vehicle_year=2022,
            vehicle_color='Black',
            current_latitude=40.7128,
            current_longitude=-74.0060,
            is_available=True
        )
        self.driver.save()
        
        # Otro driver
        self.other_driver = Driver(
            user_ptr_id=self.other_driver_user.id,
            username=self.other_driver_user.username,
            email=self.other_driver_user.email,
            password=self.other_driver_user.password,
            first_name=self.other_driver_user.first_name,
            last_name=self.other_driver_user.last_name,
            phone_number=self.other_driver_user.phone_number,
            is_staff=self.other_driver_user.is_staff,
            is_active=self.other_driver_user.is_active,
            date_joined=self.other_driver_user.date_joined,
            vehicle_plate='PERM456',
            vehicle_model='BMW X5',
            vehicle_year=2021,
            vehicle_color='White',
            current_latitude=40.7330,
            current_longitude=-74.0060,
            is_available=True
        )
        self.other_driver.save()
        
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
        
        # Create services
        self.client_service = Service.objects.create(
            client=self.client_user,
            driver=self.driver,
            pickup_address=self.address,
            status='IN_PROGRESS'
        )
        
        # Request factory
        self.factory = APIRequestFactory()
        
        # Permission
        self.permission = ServicePermission()
        
        # Mock view for testing - add action attribute
        self.view = type('TestView', (APIView,), {'kwargs': {'pk': self.client_service.pk}, 'action': None})()

    def test_admin_has_full_permission(self):
        """Test that admin users have full permission."""
        request = self.factory.get('/')
        request.user = self.admin_user
        
        # Admin can view
        self.assertTrue(self.permission.has_permission(request, self.view))
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Admin can create
        request = self.factory.post('/')
        request.user = self.admin_user
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_client_has_permission_to_own_services(self):
        """Test that clients have permission to their own services."""
        # Client can view own service
        request = self.factory.get('/')
        request.user = self.client_user
        self.assertTrue(self.permission.has_permission(request, self.view))
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Client can create service
        request = self.factory.post('/')
        request.user = self.client_user
        self.assertTrue(self.permission.has_permission(request, self.view))
        
        # Client cannot access another client's service
        request = self.factory.get('/')
        request.user = self.other_client_user
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.client_service))

    def test_driver_has_permission_to_assigned_services(self):
        """Test that drivers have permission to services assigned to them."""
        # Driver can view service assigned to them
        request = self.factory.get('/')
        request.user = self.driver_user
        self.assertTrue(self.permission.has_permission(request, self.view))
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Driver cannot access service assigned to another driver
        request = self.factory.get('/')
        request.user = self.other_driver_user
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Driver cannot create service
        request = self.factory.post('/')
        request.user = self.driver_user
        self.assertTrue(self.permission.has_permission(request, self.view))

    def test_driver_complete_service_permission(self):
        """Test driver permission for the complete action."""
        # Set the action to 'complete'
        self.view.action = 'complete'
        
        # Driver can complete their own assigned service
        request = self.factory.patch('/')
        request.user = self.driver_user
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Another driver cannot complete a service assigned to a different driver
        request = self.factory.patch('/')
        request.user = self.other_driver_user
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Client cannot complete their own service
        request = self.factory.patch('/')
        request.user = self.client_user
        self.assertFalse(self.permission.has_object_permission(request, self.view, self.client_service))
        
        # Admin can complete any service
        request = self.factory.patch('/')
        request.user = self.admin_user
        self.assertTrue(self.permission.has_object_permission(request, self.view, self.client_service))