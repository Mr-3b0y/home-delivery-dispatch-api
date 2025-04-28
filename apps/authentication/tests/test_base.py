from rest_framework.test import APITestCase
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticationBaseTestCase(APITestCase):
    """Base test case for authentication tests."""

    def setUp(self):
        """Set up test data."""
        self.username = 'testuser'
        self.email = 'test@example.com'
        self.password = 'testpassword123'
        self.phone_number = '+1234567890'
        
        # Create a test user
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            phone_number=self.phone_number
        )
        
        # Generate tokens for the user
        refresh = RefreshToken.for_user(self.user)
        self.refresh_token = str(refresh)
        self.access_token = str(refresh.access_token)
        
    def get_authorization_header(self):
        """Return the Authorization header with the access token."""
        return {'Authorization': f'Bearer {self.access_token}'}