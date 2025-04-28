from django.test import TestCase
from apps.users.api.v1.serializers import UserSerializer, RegisterSerializer, UserDetailSerializer
from apps.users.models import User
from rest_framework.exceptions import ValidationError


class UserSerializerTest(TestCase):
    """Tests for the user serializer"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'First',
            'last_name': 'Last',
            'phone_number': '+34612345678',
            'is_active': True,
            'is_staff': False
        }
        
    def test_validation_ok(self):
        """Test that a serializer with valid data validates correctly"""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        
    def test_different_passwords(self):
        """Test that both passwords must match"""
        data = self.user_data.copy()
        data['password2'] = 'different_password'
        
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password2', serializer.errors)
        
    def test_create_user(self):
        """Test user creation through the serializer"""
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password1']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])
        
    def test_update_user(self):
        """Test user update through the serializer"""
        # First create a user
        user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password1'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            phone_number=self.user_data['phone_number']
        )
        
        # Data to update
        update_data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'password1': 'new_password',
            'password2': 'new_password'
        }
        
        serializer = UserSerializer(instance=user, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_user = serializer.save()
        self.assertEqual(updated_user.first_name, update_data['first_name'])
        self.assertEqual(updated_user.last_name, update_data['last_name'])
        self.assertTrue(updated_user.check_password(update_data['password1']))


class RegisterSerializerTest(TestCase):
    """Tests for the registration serializer"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.registration_data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'password': 'Secure_Password_789!',
            'password2': 'Secure_Password_789!',
            'first_name': 'First',
            'last_name': 'Last',
            'phone_number': '+34612345678'
        }
        
    def test_validation_ok(self):
        """Test that a serializer with valid data validates correctly"""
        serializer = RegisterSerializer(data=self.registration_data)
        is_valid = serializer.is_valid()
        if not is_valid:
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(is_valid)
        
    def test_different_passwords(self):
        """Test that both passwords must match"""
        data = self.registration_data.copy()
        data['password2'] = 'different_password'
        
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        
    def test_unique_email(self):
        """Test that the email must be unique"""
        # Create user first
        User.objects.create_user(
            username='existing_user',
            email=self.registration_data['email'],
            password='Secure_Password_789!',
            phone_number='+34611111111'
        )
        
        serializer = RegisterSerializer(data=self.registration_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        
    def test_create_user(self):
        """Test user creation through the registration serializer"""
        serializer = RegisterSerializer(data=self.registration_data)
        is_valid = serializer.is_valid()
        if not is_valid:
            print(f"Create user validation errors: {serializer.errors}")
        self.assertTrue(is_valid)
        
        user = serializer.save()
        self.assertEqual(user.username, self.registration_data['username'])
        self.assertEqual(user.email, self.registration_data['email'])
        self.assertTrue(user.check_password(self.registration_data['password']))
        self.assertEqual(user.first_name, self.registration_data['first_name'])
        self.assertEqual(user.last_name, self.registration_data['last_name'])
        self.assertEqual(user.phone_number, self.registration_data['phone_number'])


class UserDetailSerializerTest(TestCase):
    """Tests for the user detail serializer"""
    
    def setUp(self):
        """Initial setup for tests"""
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password123',
            first_name='First',
            last_name='Last',
            phone_number='+34612345678'
        )
        
    def test_serialization(self):
        """Test serialization of an existing user"""
        serializer = UserDetailSerializer(instance=self.user)
        data = serializer.data
        
        self.assertEqual(data['id'], self.user.id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['first_name'], self.user.first_name)
        self.assertEqual(data['last_name'], self.user.last_name)
        self.assertEqual(data['phone_number'], self.user.phone_number)
        self.assertEqual(data['is_active'], self.user.is_active)
        self.assertEqual(data['is_staff'], self.user.is_staff)
        
        # Verify that read-only fields are not in the data for writing
        self.assertNotIn('password', data) 