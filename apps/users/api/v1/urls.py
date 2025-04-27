from rest_framework.routers import DefaultRouter

from apps.users.api.v1 import views as v


router = DefaultRouter()
router.register(r'users', v.UserViewSet, basename='user')


urlpatterns = router.urls