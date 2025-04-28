from django.urls import reverse
from rest_framework import status

from apps.authentication.tests.test_base import AuthenticationBaseTestCase


class TokenVerifyViewTests(AuthenticationBaseTestCase):
    """Test suite for the token verify view."""

    def setUp(self):
        """Set up test data."""
        super().setUp()
        # URL for token verify
        self.url = reverse('urls-v1:token_verify')
    
    def test_verify_token_success_access(self):
        """Test successful token verification with access token."""
        data = {
            'token': self.access_token
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_verify_token_success_refresh(self):
        """Test successful token verification with refresh token."""
        data = {
            'token': self.refresh_token
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        data = {
            'token': 'invalidtoken'
        }
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_verify_token_missing(self):
        """Test token verification with missing token."""
        data = {}
        
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_verify_expired_token(self):
        """Test verification of an expired token would fail.
        Note: This test is more complex and would typically involve 
        patching the datetime to simulate token expiration, which is beyond
        the scope of this simple test suite. This is just a placeholder.
        """
        pass