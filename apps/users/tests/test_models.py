from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.users.models import User
from django.db.utils import IntegrityError
from django.db import transaction


class UserModelTest(TestCase):
    """Tests for the user model"""

    def setUp(self):
        """Initial setup for tests"""
        self.user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'First',
            'last_name': 'Last',
            'phone_number': '+34612345678'
        }
        
    def test_create_user(self):
        """Test creating a normal user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        
    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(**self.user_data)
        self.assertEqual(admin.username, self.user_data['username'])
        self.assertEqual(admin.email, self.user_data['email'])
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        
    def test_create_user_without_email(self):
        """Test that a user cannot be created with an empty email"""
        empty_email_data = self.user_data.copy()
        empty_email_data['email'] = ''
        
        with self.assertRaises(ValueError):
            User.objects.create_user(**empty_email_data)
            
    def test_create_superuser_without_is_staff(self):
        """Test that a superuser cannot be created with is_staff=False"""
        data = self.user_data.copy()
        data['is_staff'] = False
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(**data)
            
    def test_create_superuser_without_is_superuser(self):
        """Test that a superuser cannot be created with is_superuser=False"""
        data = self.user_data.copy()
        data['is_superuser'] = False
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(**data)
            
    def test_user_str(self):
        """Test the string representation of the user"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])
        
    def test_unique_phone(self):
        """Test that the phone number must be unique"""
        # Create the first user
        User.objects.create_user(**self.user_data)
        
        # Try to create another user with the same phone number
        second_user_data = self.user_data.copy()
        second_user_data['username'] = 'another_user'
        second_user_data['email'] = 'another@example.com'
        
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                User.objects.create_user(**second_user_data)
                
    def test_valid_phone_format(self):
        """Test that the phone number must have a valid format"""
        invalid_phone_data = self.user_data.copy()
        invalid_phone_data['phone_number'] = 'not-a-phone'
        
        user = User(**invalid_phone_data)
        with self.assertRaises(ValidationError):
            user.full_clean() 