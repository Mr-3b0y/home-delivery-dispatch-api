from rest_framework import serializers
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number', 'is_active', 'is_staff')
        read_only_fields = ('id',)
        
    def validate(self, data):
        """
        Validate that both passwords match if provided.
        """
        # Solo verificar las contraseñas si ambas están presentes en los datos
        if 'password1' in data and 'password2' in data:
            if data['password1'] != data['password2']:
                raise serializers.ValidationError({"password2": _("Passwords do not match.")})
        
        # Si solo una de las contraseñas está presente, es un error
        elif 'password1' in data and 'password2' not in data:
            raise serializers.ValidationError({"password2": _("Password confirmation required.")})
        elif 'password2' in data and 'password1' not in data:
            raise serializers.ValidationError({"password1": _("Password required.")})
            
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
            validated_data.pop('password2', None)  # Eliminar password2 si existe
            instance.set_password(password)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
        
        
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
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'last_login', 'phone_number')
        read_only_fields = ('id', 'is_active', 'is_staff', 'email', 'username', 'date_joined', 'last_login')