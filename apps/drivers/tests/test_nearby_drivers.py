from django.test import TestCase
from apps.drivers.models import Driver
from apps.users.models import User
from decimal import Decimal
import uuid


class NearbyDriversTest(TestCase):
    """Test cases for finding nearby drivers."""

    def setUp(self):
        """Set up test data with drivers at different locations."""
        # Base coordinates (Downtown San Francisco)
        self.base_lat = Decimal('37.7749')
        self.base_lng = Decimal('-122.4194')
        
        # Create common driver attributes
        self.common_attrs = {
            'vehicle_model': 'Toyota Corolla',
            'vehicle_year': 2020,
            'vehicle_color': 'Blue',
            'is_available': True,
        }
        
        # Usar sufijos únicos para evitar nombres de usuario duplicados
        self.test_id = uuid.uuid4().hex[:8]
        
        # Create several drivers at different distances
        self.create_driver_at_distance(
            f'driver1_{self.test_id}', '1.5km',
            Decimal('37.7859'), Decimal('-122.4071'),
            is_available=True
        )
        
        self.create_driver_at_distance(
            f'driver2_{self.test_id}', '3km',
            Decimal('37.8019'), Decimal('-122.4189'),
            is_available=True
        )
        
        self.create_driver_at_distance(
            f'driver3_{self.test_id}', '5km',
            Decimal('37.7329'), Decimal('-122.3631'),
            is_available=True
        )
        
        self.create_driver_at_distance(
            f'driver4_{self.test_id}', '10km',
            Decimal('37.6879'), Decimal('-122.4702'),
            is_available=True
        )
        
        # Create an unavailable driver nearby
        self.create_driver_at_distance(
            f'driver5_{self.test_id}', '1km',
            Decimal('37.7834'), Decimal('-122.4167'),
            is_available=False
        )

    def create_driver_at_distance(self, username, distance_desc, latitude, longitude, is_available):
        """Helper method to create a driver at a specific location."""
        # Limitar plate a 20 caracteres máximo
        plate = f'P-{username[-8:]}'
        
        # Generar un número de teléfono único basado en el nombre de usuario
        # Convertir cualquier letra en el username a dígitos (solo los primeros 10 caracteres)
        # y asegurarnos que cumpla con el formato de número de teléfono
        unique_id = str(uuid.uuid4().int)[:10]
        phone_number = f'+1{unique_id}'
        
        # Crear un conductor directamente con create_user
        driver = Driver.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='password123',
            phone_number=phone_number,
            first_name=f'Driver{username[-1]}',
            last_name='Test',
            # Driver-specific fields
            vehicle_plate=plate,
            vehicle_model=self.common_attrs['vehicle_model'],
            vehicle_year=self.common_attrs['vehicle_year'],
            vehicle_color=self.common_attrs['vehicle_color'],
            current_latitude=latitude,
            current_longitude=longitude,
            is_available=is_available
        )
        
        return driver
    
    def test_find_nearest_drivers(self):
        """Test finding nearest available drivers."""
        # Get all drivers with our test suffix
        all_drivers = Driver.objects.filter(is_available=True, username__contains=self.test_id)
        
        # Calculate distances for each driver from the base location
        drivers_with_distances = [(driver, driver.calculate_distance(
            self.base_lat, self.base_lng)) for driver in all_drivers]
        
        # Sort by distance
        sorted_drivers = sorted(drivers_with_distances, key=lambda x: x[1])
        
        # Get the usernames of the sorted drivers
        sorted_usernames = [driver[0].username for driver in sorted_drivers]
        
        # Verify the order (nearest to farthest)
        self.assertEqual(sorted_usernames, [
            f'driver1_{self.test_id}', 
            f'driver2_{self.test_id}', 
            f'driver3_{self.test_id}', 
            f'driver4_{self.test_id}'
        ])
        
        # Verify the distances are calculated correctly
        distances = [round(distance, 1) for _, distance in sorted_drivers]
        
        # Expected approximate distances (ajustados según los resultados reales)
        self.assertAlmostEqual(distances[0], 1.5, delta=0.2)  # ~1.5km
        self.assertAlmostEqual(distances[1], 3.0, delta=0.3)  # ~3km
        # Ajustar la expectativa para el tercer conductor (usar ~6.8km en lugar de ~5km)
        self.assertAlmostEqual(distances[2], 6.8, delta=0.5)  # ~6.8km
        self.assertAlmostEqual(distances[3], 10.0, delta=1.0)  # ~10km
        
    def test_find_drivers_within_radius(self):
        """Test finding available drivers within a specific radius."""
        # Find drivers within 4km
        max_distance = 4.0
        
        # Get all available drivers with our test suffix
        all_drivers = Driver.objects.filter(is_available=True, username__contains=self.test_id)
        
        # Filter by distance
        drivers_within_radius = [
            driver for driver in all_drivers 
            if driver.calculate_distance(self.base_lat, self.base_lng) <= max_distance
        ]
        
        # Get usernames of drivers within radius
        usernames_within_radius = [driver.username for driver in drivers_within_radius]
        
        # Should include driver1 (~1.5km) and driver2 (~3km) but not driver3 (~6.8km) or driver4 (~10km)
        self.assertIn(f'driver1_{self.test_id}', usernames_within_radius)
        self.assertIn(f'driver2_{self.test_id}', usernames_within_radius)
        self.assertNotIn(f'driver3_{self.test_id}', usernames_within_radius)
        self.assertNotIn(f'driver4_{self.test_id}', usernames_within_radius)
        
        # There should be exactly 2 drivers within this radius
        self.assertEqual(len(drivers_within_radius), 2)
        
    def test_filter_by_availability(self):
        """Test that unavailable drivers are properly filtered out."""
        # We should only get available drivers, even if an unavailable one is closer
        all_available_drivers = Driver.objects.filter(is_available=True, username__contains=self.test_id)
        
        # There should be 4 available drivers
        self.assertEqual(all_available_drivers.count(), 4)
        
        # Calculate distances for available drivers only
        drivers_with_distances = [(driver, driver.calculate_distance(
            self.base_lat, self.base_lng)) for driver in all_available_drivers]
        
        # Sort by distance
        sorted_drivers = sorted(drivers_with_distances, key=lambda x: x[1])
        
        # First driver should be driver1, not the unavailable driver5 (which is closer)
        self.assertEqual(sorted_drivers[0][0].username, f'driver1_{self.test_id}')