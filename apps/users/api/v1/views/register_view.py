from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from apps.users.api.v1.serializers import RegisterSerializer
from apps.users.models import User


@extend_schema_view(
    post=extend_schema(
        tags=["User Registration"],
        summary="Register a new user",
))
class RegisterView(generics.CreateAPIView):  
    """
    API view to register a new user.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    