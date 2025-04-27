from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.users.api.v1.serializers import RegisterSerializer
from apps.users.models import User


class RegisterView(generics.CreateAPIView):  
    """
    API view to register a new user.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    