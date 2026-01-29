"""
Serializers for Rating models
"""
from rest_framework import serializers
from .models import Review
from apps.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    reviewer_details = UserSerializer(source='reviewer', read_only=True)
    reviewed_user_details = UserSerializer(source='reviewed_user', read_only=True)
    trip_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'id', 'trip', 'reviewer', 'reviewed_user',
            'reviewer_details', 'reviewed_user_details', 'trip_details',
            'rating', 'comment',
            'punctuality_rating', 'cleanliness_rating',
            'safety_rating', 'communication_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']
    
    def get_trip_details(self, obj):
        return {
            'id': obj.trip.id,
            'start_location': obj.trip.start_location_name,
            'end_location': obj.trip.end_location_name,
            'completed_at': obj.trip.completed_at
        }


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new review"""
    
    class Meta:
        model = Review
        fields = [
            'trip', 'reviewed_user', 'rating', 'comment',
            'punctuality_rating', 'cleanliness_rating',
            'safety_rating', 'communication_rating'
        ]
    
    def validate(self, attrs):
        trip = attrs.get('trip')
        reviewer = self.context['request'].user
        reviewed_user = attrs.get('reviewed_user')
        
        # Check if trip is completed
        if trip.status != 'completed':
            raise serializers.ValidationError("Can only review completed trips.")
        
        # Check if reviewer is part of the trip
        if reviewer not in [trip.passenger, trip.driver]:
            raise serializers.ValidationError("You can only review trips you were part of.")
        
        # Check if reviewed_user is the other party in the trip
        if reviewed_user == reviewer:
            raise serializers.ValidationError("You cannot review yourself.")
        
        if reviewed_user not in [trip.passenger, trip.driver]:
            raise serializers.ValidationError("You can only review the other party in the trip.")
        
        # Check if review already exists
        if Review.objects.filter(trip=trip, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this trip.")
        
        return attrs
    
    def create(self, validated_data):
        # Set the reviewer to the current user
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class UserReviewSummarySerializer(serializers.Serializer):
    """Serializer for user review summary statistics"""
    user_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_null=True)
    total_reviews = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    five_star_count = serializers.IntegerField()
    four_star_count = serializers.IntegerField()
    three_star_count = serializers.IntegerField()
    two_star_count = serializers.IntegerField()
    one_star_count = serializers.IntegerField()
