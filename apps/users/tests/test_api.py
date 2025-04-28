from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User
import json


class RegisterViewTest(TestCase):
    """Tests for the user registration view"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.client = APIClient()
        self.register_url = reverse('urls-v1:register')
        self.user_data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'password': 'Secure_Password_789!',
            'password2': 'Secure_Password_789!',
            'first_name': 'First',
            'last_name': 'Last',
            'phone_number': '+34612345678'
        }
        
    def test_successful_registration(self):
        """Test a successful user registration"""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify that the user was created in the database
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())
        
    def test_registration_without_required_data(self):
        """Test that registration fails if required data is missing"""
        incomplete_data = {
            'username': 'new_user',
            'email': 'new@example.com'
        }
        
        response = self.client.post(self.register_url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_with_existing_email(self):
        """Test that registration fails if the email already exists"""
        # Create a user first
        User.objects.create_user(
            username='existing_user',
            email=self.user_data['email'],
            password='Secure_Password_789!',
            phone_number='+34611111111'
        )
        
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserViewSetTest(TestCase):
    """Tests for the User ViewSet"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.client = APIClient()
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            phone_number='+34699999999'
        )
        
        # Create normal user
        self.normal_user = User.objects.create_user(
            username='normal',
            email='normal@example.com',
            password='normal123',
            phone_number='+34688888888'
        )
        
        # Create URLs
        self.list_url = reverse('urls-v1:user-list')
        self.detail_url = reverse('urls-v1:user-detail', kwargs={'pk': self.normal_user.pk})
        
    def test_list_users_as_admin(self):
        """Test that an admin can list all users"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), 2)  # Admin and normal user
        
    def test_list_users_unauthenticated(self):
        """Test that an unauthenticated user cannot list users"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_list_users_as_normal_user(self):
        """Test that a normal user cannot list users (not admin)"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_detail_user_as_admin(self):
        """Test that an admin can view a user's details"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.normal_user.username)
        self.assertEqual(response.data['email'], self.normal_user.email)
        
    def test_create_user_as_admin(self):
        """Test creating a user through the API"""
        self.client.force_authenticate(user=self.admin_user)
        
        new_user_data = {
            'username': 'another_user',
            'email': 'another_123@example.com',
            'password1': 'Secure_Password_789!',
            'password2': 'Secure_Password_789!',
            'first_name': 'Another',
            'last_name': 'User',
            'phone_number': '+346777777347',
            'is_active': True
        }
        
        response = self.client.post(self.list_url, new_user_data, format='json')
      
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify that the user was created in the database
        self.assertTrue(User.objects.filter(username='another_user').exists())
        
    def test_update_user_as_admin(self):
        """Test updating a user through the API"""
        self.client.force_authenticate(user=self.admin_user)
        
        update_data = {
            'first_name': 'UpdatedFirstName',
            'last_name': 'UpdatedLastName'
        }
        
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload user from database
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.first_name, 'UpdatedFirstName')
        self.assertEqual(self.normal_user.last_name, 'UpdatedLastName')
        
    def test_delete_user_as_admin(self):
        """Test deleting a user through the API"""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify that the user was deleted from the database
        self.assertFalse(User.objects.filter(pk=self.normal_user.pk).exists())


class MeViewTest(TestCase):
    """Tests for the authenticated user profile view"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.client = APIClient()
        
        # Create user
        self.user = User.objects.create_user(
            username='username',
            email='user@example.com',
            password='user123',
            first_name='First',
            last_name='Last',
            phone_number='+34655555555'
        )
        
        # Profile view URL
        self.me_url = reverse('urls-v1:me')
        
    def test_get_authenticated_profile(self):
        """Test that an authenticated user can get their profile"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        
    def test_get_profile_unauthenticated(self):
        """Test that an unauthenticated user cannot get the profile"""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_profile(self):
        """Test that an authenticated user can update their profile"""
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName'
        }
        
        response = self.client.patch(self.me_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.last_name, 'NewLastName')
        
    def test_update_readonly_fields(self):
        """Test that readonly fields cannot be updated"""
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'email': 'new@example.com',
            'username': 'new_username',
            'is_staff': True
        }
        
        response = self.client.patch(self.me_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload user from database and verify that readonly fields were not updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'user@example.com')  # No change
        self.assertEqual(self.user.username, 'username')  # No change
        self.assertFalse(self.user.is_staff)  # No change 