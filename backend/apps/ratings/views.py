"""
Views for Rating management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Avg, Q

from .models import Review
from .serializers import (
    ReviewSerializer,
    ReviewCreateSerializer,
    UserReviewSummarySerializer
)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review model.
    Provides CRUD operations for reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_queryset(self):
        """Filter reviews based on query parameters"""
        queryset = Review.objects.all()
        
        # Filter by user (reviews received by user)
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(reviewed_user_id=user_id)
        
        # Filter by reviewer
        reviewer_id = self.request.query_params.get('reviewer_id', None)
        if reviewer_id:
            queryset = queryset.filter(reviewer_id=reviewer_id)
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip_id', None)
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def my_reviews_received(self, request):
        """Get reviews received by current user"""
        reviews = Review.objects.filter(reviewed_user=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_reviews_given(self, request):
        """Get reviews given by current user"""
        reviews = Review.objects.filter(reviewer=request.user)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def user_summary(self, request):
        """Get review summary for a user"""
        user_id = request.query_params.get('user_id', request.user.id)
        
        reviews = Review.objects.filter(reviewed_user_id=user_id)
        
        if not reviews.exists():
            return Response({
                'user_id': user_id,
                'total_reviews': 0,
                'average_rating': None,
                'five_star_count': 0,
                'four_star_count': 0,
                'three_star_count': 0,
                'two_star_count': 0,
                'one_star_count': 0,
            })
        
        summary = {
            'user_id': user_id,
            'username': reviews.first().reviewed_user.username,
            'total_reviews': reviews.count(),
            'average_rating': reviews.aggregate(Avg('rating'))['rating__avg'],
            'five_star_count': reviews.filter(rating=5).count(),
            'four_star_count': reviews.filter(rating=4).count(),
            'three_star_count': reviews.filter(rating=3).count(),
            'two_star_count': reviews.filter(rating=2).count(),
            'one_star_count': reviews.filter(rating=1).count(),
        }
        
        serializer = UserReviewSummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending_reviews(self, request):
        """Get trips that need to be reviewed by current user"""
        from apps.trips.models import Trip
        
        # Get completed trips where user was involved
        completed_trips = Trip.objects.filter(
            Q(passenger=request.user) | Q(driver=request.user),
            status='completed'
        )
        
        # Filter out trips that have already been reviewed by the user
        reviewed_trip_ids = Review.objects.filter(
            reviewer=request.user
        ).values_list('trip_id', flat=True)
        
        pending_trips = completed_trips.exclude(id__in=reviewed_trip_ids)
        
        # Prepare response with trip details
        result = []
        for trip in pending_trips:
            # Determine who to review
            if request.user == trip.passenger and trip.driver:
                to_review = trip.driver
            elif request.user == trip.driver:
                to_review = trip.passenger
            else:
                continue
            
            result.append({
                'trip_id': trip.id,
                'trip_details': {
                    'start_location': trip.start_location_name,
                    'end_location': trip.end_location_name,
                    'completed_at': trip.completed_at
                },
                'user_to_review': {
                    'id': to_review.id,
                    'username': to_review.username,
                    'full_name': to_review.get_full_name()
                }
            })
        
        return Response(result)
