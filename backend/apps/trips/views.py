"""
Views for Trip management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

from .models import Trip
from .serializers import (
    TripSerializer,
    TripCreateSerializer,
    TripUpdateSerializer,
    TripHistorySerializer
)


class TripViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Trip model.
    Provides CRUD operations for trips.
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TripCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TripUpdateSerializer
        elif self.action in ['my_trips', 'trip_history']:
            return TripHistorySerializer
        return TripSerializer
    
    def get_queryset(self):
        """Filter trips based on user role"""
        user = self.request.user
        if user.is_staff:
            return Trip.objects.all()
        
        # Return trips where user is either passenger or driver
        return Trip.objects.filter(
            Q(passenger=user) | Q(driver=user)
        )
    
    @action(detail=False, methods=['get'])
    def my_trips(self, request):
        """Get current user's active trips"""
        trips = Trip.objects.filter(
            Q(passenger=request.user) | Q(driver=request.user)
        ).exclude(status__in=['completed', 'cancelled'])
        
        serializer = self.get_serializer(trips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trip_history(self, request):
        """Get current user's trip history"""
        role = request.query_params.get('role', 'all')
        
        if role == 'passenger':
            trips = Trip.objects.filter(
                passenger=request.user,
                status='completed'
            )
        elif role == 'driver':
            trips = Trip.objects.filter(
                driver=request.user,
                status='completed'
            )
        else:
            trips = Trip.objects.filter(
                Q(passenger=request.user) | Q(driver=request.user),
                status='completed'
            )
        
        serializer = self.get_serializer(trips, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_trips(self, request):
        """Get pending trips (for drivers to accept)"""
        if not hasattr(request.user, 'driver_profile'):
            return Response(
                {'detail': 'Only drivers can view pending trips.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        trips = Trip.objects.filter(status='pending')
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a trip (driver only)"""
        trip = self.get_object()
        
        if not hasattr(request.user, 'driver_profile'):
            return Response(
                {'detail': 'Only drivers can accept trips.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if trip.status != 'pending':
            return Response(
                {'detail': 'Trip is not available for acceptance.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.driver = request.user
        trip.status = 'accepted'
        trip.accepted_at = timezone.now()
        trip.save()
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a trip (driver only)"""
        trip = self.get_object()
        
        if trip.driver != request.user:
            return Response(
                {'detail': 'Only the assigned driver can start this trip.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if trip.status != 'accepted':
            return Response(
                {'detail': 'Trip must be accepted before starting.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.status = 'in_progress'
        trip.started_at = timezone.now()
        trip.save()
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete a trip (driver only)"""
        trip = self.get_object()
        
        if trip.driver != request.user:
            return Response(
                {'detail': 'Only the assigned driver can complete this trip.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if trip.status != 'in_progress':
            return Response(
                {'detail': 'Trip must be in progress to complete.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.complete_trip()
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a trip"""
        trip = self.get_object()
        
        # Only passenger or assigned driver can cancel
        if trip.passenger != request.user and trip.driver != request.user:
            return Response(
                {'detail': 'Only passenger or assigned driver can cancel this trip.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if trip.status in ['completed', 'cancelled']:
            return Response(
                {'detail': 'Cannot cancel a completed or already cancelled trip.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        trip.status = 'cancelled'
        trip.cancelled_at = timezone.now()
        trip.save()
        
        serializer = TripSerializer(trip)
        return Response(serializer.data)
