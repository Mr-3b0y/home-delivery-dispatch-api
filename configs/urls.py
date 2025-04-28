"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urls_v1 = [
    path('users/', include('apps.users.api.v1.urls')),
    path('auth/', include('apps.authentication.api.v1.urls')),
    path('drivers/', include('apps.drivers.api.v1.urls')),
    path('addresses/', include('apps.addresses.api.v1.urls')),
    path('services/', include('apps.services.api.v1.urls')),
]

urls_v2 = [
    # path('v2/', include('apps.users.api.v2.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        "api/",
        include(
            [
                path("v1/", include((urls_v1, "v1"), namespace="urls-v1")),
                path("v2/", include((urls_v2, "v2"), namespace="urls-v2")),
                # path("docs/", include("docs.swagger.urls")),
            ]
        ),
    ),
    
    # Documentation URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
