"""
Serializers for Trip models
"""
from rest_framework import serializers
from .models import Trip
from apps.users.serializers import UserSerializer


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model"""
    passenger_details = UserSerializer(source='passenger', read_only=True)
    driver_details = UserSerializer(source='driver', read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'passenger', 'driver', 'passenger_details', 'driver_details',
            'start_location_name', 'start_latitude', 'start_longitude',
            'end_location_name', 'end_latitude', 'end_longitude',
            'status', 'distance_km', 'estimated_duration_minutes', 'fare',
            'requested_at', 'accepted_at', 'started_at', 'completed_at', 'cancelled_at',
            'passenger_notes', 'driver_notes', 'number_of_passengers',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'passenger', 'requested_at', 'accepted_at', 'started_at',
            'completed_at', 'cancelled_at', 'created_at', 'updated_at'
        ]


class TripCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new trip"""
    
    class Meta:
        model = Trip
        fields = [
            'start_location_name', 'start_latitude', 'start_longitude',
            'end_location_name', 'end_latitude', 'end_longitude',
            'passenger_notes', 'number_of_passengers'
        ]
    
    def create(self, validated_data):
        # Set the passenger to the current user
        validated_data['passenger'] = self.context['request'].user
        return super().create(validated_data)


class TripUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating trip status"""
    
    class Meta:
        model = Trip
        fields = ['status', 'driver_notes']


class TripHistorySerializer(serializers.ModelSerializer):
    """Simplified serializer for trip history"""
    passenger_name = serializers.CharField(source='passenger.get_full_name', read_only=True)
    driver_name = serializers.SerializerMethodField()
    has_passenger_review = serializers.SerializerMethodField()
    has_driver_review = serializers.SerializerMethodField()
    
    class Meta:
        model = Trip
        fields = [
            'id', 'passenger_name', 'driver_name',
            'start_location_name', 'end_location_name',
            'status', 'distance_km', 'fare',
            'requested_at', 'completed_at',
            'has_passenger_review', 'has_driver_review'
        ]
    
    def get_driver_name(self, obj):
        """Get driver name, handling null driver"""
        return obj.driver.get_full_name() if obj.driver else None
    
    def get_has_passenger_review(self, obj):
        """Check if passenger has reviewed this trip"""
        from apps.ratings.models import Review
        return Review.objects.filter(
            trip=obj,
            reviewer=obj.passenger
        ).exists()
    
    def get_has_driver_review(self, obj):
        """Check if driver has reviewed this trip"""
        from apps.ratings.models import Review
        if obj.driver:
            return Review.objects.filter(
                trip=obj,
                reviewer=obj.driver
            ).exists()
        return False
