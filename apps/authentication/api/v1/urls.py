from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


from apps.authentication.api.v1 import views as v

router = DefaultRouter()


urlpatterns = [
    path('login/', v.CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
