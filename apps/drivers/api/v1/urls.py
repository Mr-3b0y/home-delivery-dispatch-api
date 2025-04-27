from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.drivers.api.v1 import views as v


router = DefaultRouter()
router.register(r'drivers', v.DriverViewSet, basename='driver')


urlpatterns = [
    path('', include(router.urls)),
]