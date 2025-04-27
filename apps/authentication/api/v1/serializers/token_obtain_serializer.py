from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to add additional claims to the JWT token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_staff'] = user.is_staff
        token['is_driver'] = user.is_driver
        token['is_client'] = user.is_client
        return token