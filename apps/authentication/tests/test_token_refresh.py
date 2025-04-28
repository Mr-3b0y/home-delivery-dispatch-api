from django.urls import reverse
from rest_framework import status

from apps.authentication.tests.test_base import AuthenticationBaseTestCase


class TokenRefreshViewTests(AuthenticationBaseTestCase):
    """Test suite for the token refresh view."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        # URL for token refresh
        self.url = reverse('urls-v1:token_refresh')
    
    def test_refresh_token_success(self):
        """Test successful token refresh."""
        data = {
            'refresh': self.refresh_token
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
    def test_refresh_token_invalid(self):
        """Test token refresh with invalid token."""
        data = {
            'refresh': 'invalidtoken'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_refresh_token_missing(self):
        """Test token refresh with missing token."""
        data = {}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)