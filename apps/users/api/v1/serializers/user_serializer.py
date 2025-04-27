from rest_framework import serializers
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        read_only_fields = ('id',)
        
    def validate(self, data):
        """
        Validate that both passwords match.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": _("Passwords do not match.")})
        return data
        
    def create(self, validated_data):
        """
        Create a new user instance.
        """
        # Remove password2 as it's just for validation
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    

    def update(self, instance, validated_data):
        """
        Update an existing user instance.
        """
        # Check if password is provided in the update
        password = validated_data.pop('password1', None)
        if password:
            instance.set_password(password)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
class UserLoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.
    """
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        
class UserChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(_("New password and confirm password do not match."))
        return attrs
    
class UserResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for resetting user password.
    """
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("User with this email does not exist."))
        return value
    
class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for user details.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
        read_only_fields = ('id',)