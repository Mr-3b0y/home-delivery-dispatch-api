from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }
    
    def validate(self, data):
        """
        Validate that both passwords match.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')  # Remove password2 as it's just for validation
        password = validated_data.pop('password1')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return super().create(validated_data)