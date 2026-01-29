"""
URL patterns for users app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet, PassengerProfileViewSet, DriverProfileViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')
router.register(r'passengers', PassengerProfileViewSet, basename='passenger')
router.register(r'drivers', DriverProfileViewSet, basename='driver')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
