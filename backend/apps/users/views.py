"""
Views for User management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .models import PassengerProfile, DriverProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserUpdateSerializer,
    PassengerProfileSerializer,
    DriverProfileSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PassengerProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PassengerProfile model.
    """
    queryset = PassengerProfile.objects.all()
    serializer_class = PassengerProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own passenger profile
        if self.request.user.is_staff:
            return PassengerProfile.objects.all()
        return PassengerProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's passenger profile"""
        try:
            profile = PassengerProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except PassengerProfile.DoesNotExist:
            return Response(
                {'detail': 'Passenger profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class DriverProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DriverProfile model.
    """
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own driver profile
        if self.request.user.is_staff:
            return DriverProfile.objects.all()
        return DriverProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's driver profile"""
        try:
            profile = DriverProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except DriverProfile.DoesNotExist:
            return Response(
                {'detail': 'Driver profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def available_drivers(self, request):
        """Get list of available drivers"""
        drivers = DriverProfile.objects.filter(is_available=True, is_verified=True)
        serializer = self.get_serializer(drivers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """Toggle driver availability"""
        profile = self.get_object()
        if profile.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Permission denied.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        profile.is_available = not profile.is_available
        profile.save()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
