from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.users.api.v1 import views as v


router = DefaultRouter()
router.register(r'user', v.UserViewSet, basename='user')


urlpatterns = [
    path('register/', v.RegisterView.as_view(), name='register'),
    path('me/', v.MeView.as_view(), name='me'),
    ] + router.urls