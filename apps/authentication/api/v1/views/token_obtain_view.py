from rest_framework_simplejwt.views import TokenObtainPairView

from apps.authentication.api.v1.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token with additional claims.
    """
    
    serializer_class = CustomTokenObtainPairSerializer