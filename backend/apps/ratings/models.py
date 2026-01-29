"""
Rating and Review models for the Euro Bakshish application.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.trips.models import Trip

User = get_user_model()


class Review(models.Model):
    """
    Model representing a review/rating given by a user after a trip.
    Both passengers and drivers can review each other.
    """
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    reviewed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_received'
    )
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    
    # Review categories (optional)
    punctuality_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    safety_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication_rating = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['trip', 'reviewer']
        indexes = [
            models.Index(fields=['reviewed_user', '-created_at']),
            models.Index(fields=['reviewer']),
        ]
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username} ({self.rating} stars)"
    
    def save(self, *args, **kwargs):
        """Override save to update user ratings after review is saved"""
        super().save(*args, **kwargs)
        
        # Update the reviewed user's rating
        if self.reviewed_user == self.trip.passenger and hasattr(self.reviewed_user, 'passenger_profile'):
            self.reviewed_user.passenger_profile.update_rating()
        elif self.reviewed_user == self.trip.driver and hasattr(self.reviewed_user, 'driver_profile'):
            self.reviewed_user.driver_profile.update_rating()
