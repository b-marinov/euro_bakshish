"""
Trip models for the Euro Bakshish application.
"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Trip(models.Model):
    """
    Model representing a trip/ride.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    passenger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='trips_as_passenger'
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trips_as_driver'
    )
    
    # Location details
    start_location_name = models.CharField(max_length=255)
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    end_location_name = models.CharField(max_length=255)
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    # Trip details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    distance_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    estimated_duration_minutes = models.IntegerField(null=True, blank=True)
    fare = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    passenger_notes = models.TextField(blank=True)
    driver_notes = models.TextField(blank=True)
    number_of_passengers = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['passenger', '-created_at']),
            models.Index(fields=['driver', '-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Trip {self.id}: {self.start_location_name} to {self.end_location_name}"
    
    def complete_trip(self):
        """Mark trip as completed and update user statistics."""
        from django.utils import timezone
        
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
        
        # Update trip counts
        if hasattr(self.passenger, 'passenger_profile'):
            profile = self.passenger.passenger_profile
            profile.total_trips += 1
            profile.save()
        
        if self.driver and hasattr(self.driver, 'driver_profile'):
            profile = self.driver.driver_profile
            profile.total_trips += 1
            profile.save()
