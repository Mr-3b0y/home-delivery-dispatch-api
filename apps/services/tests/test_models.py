from decimal import Decimal
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point

from apps.services.models import Service
from apps.users.models import User
from apps.drivers.models import Driver
from apps.addresses.models import Address


class ServiceModelTestCase(TestCase):
    """Test case for the Service model."""

    def setUp(self):
        """Set up test data."""
        # Create a client user
        self.client_user = User.objects.create_user(
            username='model_client',
            email='model_client@example.com',
            password='testpassword123',
            first_name='Client',
            last_name='User',
            phone_number='+34642345678'
        )

        # Create a driver user
        self.driver_user = User.objects.create_user(
            username='model_driver',
            email='model_driver@example.com',
            password='testpassword123',
            first_name='Driver',
            last_name='User',
            phone_number='+34642345679'
        )
        
        # Create a driver correctamente copiando los campos del usuario existente
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
            vehicle_plate='MODEL123',
            vehicle_model='Toyota Corolla',
            vehicle_year=2022,
            vehicle_color='White',
            location_coordinates=Point((-122.4194, 37.7749), srid=4326),
            is_available=True
        )
        self.driver.save()
        
        # Create a pickup address
        self.pickup_address = Address.objects.create(
            street='Test Street',
            state='Test State',
            city='Test City',
            country='Test Country',
            coordinates=Point((-122.4194, 37.7749), srid=4326),
            created_by=self.client_user
        )

    def test_create_service(self):
        """Test creating a service."""
        service = Service.objects.create(
            client=self.client_user,
            driver=self.driver,
            pickup_address=self.pickup_address,
            status='IN_PROGRESS',
            distance_km=Decimal('5.5'),
            estimated_arrival_minutes=10
        )
        
        self.assertEqual(service.client, self.client_user)
        self.assertEqual(service.driver, self.driver)
        self.assertEqual(service.pickup_address, self.pickup_address)
        self.assertEqual(service.status, 'IN_PROGRESS')
        self.assertEqual(service.distance_km, Decimal('5.5'))
        self.assertEqual(service.estimated_arrival_minutes, 10)

    def test_service_without_client(self):
        """Test that a service cannot be created without a client."""
        with self.assertRaises(IntegrityError):
            Service.objects.create(
                driver=self.driver,
                pickup_address=self.pickup_address,
                status='IN_PROGRESS'
            )

    def test_service_without_pickup_address(self):
        """Test that a service cannot be created without a pickup address."""
        with self.assertRaises(IntegrityError):
            Service.objects.create(
                client=self.client_user,
                driver=self.driver,
                status='IN_PROGRESS'
            )

    def test_service_status_choices(self):
        """Test the status choices of a service."""
        service = Service.objects.create(
            client=self.client_user,
            driver=self.driver,
            pickup_address=self.pickup_address,
            status='IN_PROGRESS'
        )
        
        # Test valid status
        service.status = 'COMPLETED'
        service.save()
        self.assertEqual(service.status, 'COMPLETED')
        
        # Test invalid status
        service.status = 'INVALID_STATUS'
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_negative_distance(self):
        """Test that a negative distance raises a validation error."""
        service = Service.objects.create(
            client=self.client_user,
            driver=self.driver,
            pickup_address=self.pickup_address,
            status='IN_PROGRESS'
        )
        
        service.distance_km = Decimal('-1.0')
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_service_without_driver(self):
        """Test that a service can be created without a driver."""
        service = Service.objects.create(
            client=self.client_user,
            pickup_address=self.pickup_address,
            status='IN_PROGRESS'
        )
        
        self.assertIsNone(service.driver)
        self.assertEqual(service.client, self.client_user)
        self.assertEqual(service.pickup_address, self.pickup_address)
        self.assertEqual(service.status, 'IN_PROGRESS') 