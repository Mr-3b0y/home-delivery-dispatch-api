from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from decimal import Decimal

from apps.users.models import User
from apps.addresses.models import Address


class AddressAPITests(APITestCase):
    """Test suite for the Address API."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            phone_number='+1234567890'
        )
        self.client.force_authenticate(user=self.user)
        self.address_data = {
            'street': 'Calle Test 123',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'postal_code': '12345',
            'latitude': '40.712776',
            'longitude': '-74.005974',
            'reference': 'Near the park'
        }
        self.url = '/api/v1/addresses/'

    def test_create_address(self):
        """Test creating an address via API"""
        response = self.client.post(self.url, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.get().city, 'Test City')
        self.assertEqual(Address.objects.get().created_by, self.user)
        
    def test_list_addresses(self):
        """Test listing addresses via API"""
        Address.objects.create(
            street='Calle Test 123',
            city='Test City',
            state='Test State',
            country='Test Country',
            postal_code='12345',
            latitude=Decimal('40.712776'),
            longitude=Decimal('-74.005974'),
            created_by=self.user
        )
        Address.objects.create(
            street='Calle Test 456',
            city='Another City',
            state='Another State',
            country='Another Country',
            postal_code='67890',
            latitude=Decimal('41.712776'),
            longitude=Decimal('-75.005974'),
            created_by=self.user
        )
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_unauthorized_access(self):
        """Test unauthorized access to address API"""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)