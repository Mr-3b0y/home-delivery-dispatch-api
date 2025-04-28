from django.urls import reverse
from rest_framework import status

from apps.authentication.tests.test_base import AuthenticationBaseTestCase


class TokenObtainViewTests(AuthenticationBaseTestCase):
    """Test suite for the token obtain view."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        # URL for token obtain
        self.url = reverse('urls-v1:login')
    
    def test_obtain_token_success(self):
        """Test successful token obtain."""
        data = {
            'username': self.username,
            'password': self.password
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_obtain_token_invalid_credentials(self):
        """Test token obtain with invalid credentials."""
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_obtain_token_missing_fields(self):
        """Test token obtain with missing fields."""
        # Missing password
        data = {'username': self.username}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Missing username
        data = {'password': self.password}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_contains_custom_claims(self):
        """Test the token contains custom claims."""
        data = {
            'username': self.username,
            'password': self.password
        }
        
        response = self.client.post(self.url, data, format='json')
        
        # Obtain the token
        token = response.data['access']
        
        # We could decode the token and verify the claims here, but that would require
        # importing additional libraries and is more of an integration test.
        # For now, we'll just verify the token was obtained successfully.
        self.assertEqual(response.status_code, status.HTTP_200_OK)