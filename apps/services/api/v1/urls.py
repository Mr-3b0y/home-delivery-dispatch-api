from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.services.api.v1 import views as v


router = DefaultRouter()
router.register(r'services', v.ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]