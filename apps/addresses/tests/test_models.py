from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.users.models import User
from apps.addresses.models import Address


class AddressModelTests(TestCase):
    """Test suite for the Address model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            phone_number='+1234567890'
        )
        self.address_data = {
            'street': 'Calle Test 123',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'postal_code': '12345',
            'latitude': Decimal('40.712776'),
            'longitude': Decimal('-74.005974'),
            'reference': 'Near the park',
            'created_by': self.user
        }

    def test_create_address(self):
        """Test creating an address"""
        address = Address.objects.create(**self.address_data)
        self.assertEqual(address.street, 'Calle Test 123')
        self.assertEqual(address.city, 'Test City')
        self.assertEqual(address.created_by, self.user)

    def test_address_str_representation(self):
        """Test the string representation of an address"""
        address = Address.objects.create(**self.address_data)
        expected_str = 'Calle Test 123, Test City, Test State, Test Country, 12345'
        self.assertEqual(str(address), expected_str)
        
    def test_invalid_coordinates(self):
        """Test validation for invalid coordinates"""
        # Test invalid latitude
        address = Address(**self.address_data)
        address.latitude = Decimal('91.0')
        with self.assertRaises(ValidationError):
            address.full_clean()
            
        # Test invalid longitude
        address = Address(**self.address_data)
        address.longitude = Decimal('181.0')
        with self.assertRaises(ValidationError):
            address.full_clean()