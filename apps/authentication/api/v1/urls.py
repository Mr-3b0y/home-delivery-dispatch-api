from rest_framework.routers import DefaultRouter
from django.urls import path, include


from apps.authentication.api.v1 import views as v

router = DefaultRouter()


urlpatterns = [
    path('login/', v.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', v.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', v.CustomTokenVerifyView.as_view(), name='token_verify'),
]
