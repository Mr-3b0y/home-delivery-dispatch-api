from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.drivers.models import Driver
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from django.contrib.gis.geos import Point
import uuid


class DriverLocationUpdateTest(TestCase):
    """Test cases for driver location updates."""

    def setUp(self):
        """Set up test data."""
        # Crear un Driver directamente con create_user
        self.driver = Driver.objects.create_user(
            username='locationdriver',
            email='location@example.com',
            password='testpassword123',
            phone_number='+1234567890',
            # Driver-specific fields
            vehicle_plate='LOC123',
            vehicle_model='Toyota Prius',
            vehicle_year=2019,
            vehicle_color='Silver',
            location_coordinates=Point((-122.4194, 37.7749), srid=4326),
            is_available=True
        )
        
        # Refresh from database
        self.driver.refresh_from_db()

    def test_update_location(self):
        """Test updating driver location."""
        # New coordinates (Moving to Golden Gate Park)
        new_longitude = -122.4862
        new_latitude = 37.7694
        new_point = Point((new_longitude, new_latitude), srid=4326)
        self.driver.location_coordinates = new_point
        self.driver.save()
        
        # Verify location was updated
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.location_coordinates.y, new_latitude)
        self.assertEqual(self.driver.location_coordinates.x, new_longitude)
        


class DriverLocationAPITest(APITestCase):
    """Test cases for driver location API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Crear un Driver directamente con create_user
        self.driver = Driver.objects.create_user(
            username='apidriver',
            email='apidriver@example.com',
            password='testpassword123',
            phone_number='+1999888777',
            # Driver-specific fields
            vehicle_plate='API123',
            vehicle_model='Honda Civic',
            vehicle_year=2020,
            vehicle_color='Black',
            location_coordinates=Point((-122.4194, 37.7749), srid=4326),
            is_available=True
        )
        
        # Refresh from database
        self.driver.refresh_from_db()
        
        # Generate token for driver
        self.driver_token = str(RefreshToken.for_user(self.driver).access_token)
        
        # Define URL for location update endpoint with namespace
        self.location_update_url = reverse('urls-v1:driver-detail', args=[self.driver.id])
        
    def test_update_location_api(self):
        """Test updating location through the API."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.driver_token}')
        
        new_longitude = Decimal('-122.4185')
        new_latitude = Decimal('37.7745')
        
        location_data = {
            'type': 'Point',
            'coordinates': [
                float(new_longitude),
                float(new_latitude)
            ],
        }
        
        response = self.client.patch(self.location_update_url, location_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
    def test_update_location_with_invalid_coordinates(self):
        """Test API validation for invalid coordinates."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.driver_token}')
        
        # Invalid latitude (out of range)
        invalid_data = {
            'location_coordinates': {
                'type': 'Point',
                'coordinates': [
                    float(-122.4185),
                    float(1000.0),  # Invalid (latitude must be -90 to 90)
                ],
            }
        }
        
        response = self.client.patch(self.location_update_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Invalid longitude (out of range)
        invalid_data = {
            'location_coordinates': {
                'type': 'Point',
                'coordinates': [
                    float(200.0),  # Invalid (longitude must be -180 to 180)
                    float(37.7745),
                ],
            }
        }
        
        response = self.client.patch(self.location_update_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_unauthorized_location_update(self):
        """Test that unauthorized users cannot update location."""
        # No authorization token
        response = self.client.patch(self.location_update_url, {
            'type': 'Point',
            'coordinates': [
                float(-122.4185),
                float(37.7745),
            ],
        }, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_wrong_driver_cannot_update_location(self):
        """Test that a driver cannot update another driver's location."""
        # Usar un nombre único para evitar conflicto con usernames anteriores
        unique_suffix = uuid.uuid4().hex[:8]
        
        # Crear el segundo conductor directamente con create_user
        other_driver = Driver.objects.create_user(
            username=f'driverUpdate_{unique_suffix}',
            email=f'driverupdate_{unique_suffix}@example.com',
            password='password123',
            phone_number=f'+1{unique_suffix}',
            # Driver-specific fields
            vehicle_plate='OTHER1',
            vehicle_model='Ford Focus',
            vehicle_year=2018,
            vehicle_color='White',
            location_coordinates=Point((-123.4194, 38.7749), srid=4326),
            is_available=True
        )
        
        # Refresh from database
        other_driver.refresh_from_db()
        
        # Generate token for other driver
        other_driver_token = str(RefreshToken.for_user(other_driver).access_token)
        
        # Try to update first driver's location using other driver's token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {other_driver_token}')
        
        response = self.client.patch(self.location_update_url, {
            'type': 'Point',
            'coordinates': [
                float(-122.4185),
                float(37.7745),
            ],
        }, format='json')
        
        # Should be forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)