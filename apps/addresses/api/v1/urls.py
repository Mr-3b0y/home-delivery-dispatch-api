from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.addresses.api.v1 import views as v

router = DefaultRouter()
router.register(r'addresses', v.AddressViewSet, basename='address')


urlpatterns = [
    path('', include(router.urls)),
]